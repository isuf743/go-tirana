<?php
/**
 * Go Tirana: marrja e mesazheve nga formulari i kontaktit.
 *
 * GET  ?token=1  -> kthen një token të nënshkruar me kohën aktuale
 * POST           -> validon dhe ruan mesazhin në private/messages.csv
 *
 * Mbrojtja nga spam-i (pa CAPTCHA dhe pa gjurmuar vizitorin):
 *   1. Fushë e fshehur ("website"): njerëzit nuk e shohin, robotët e plotësojnë.
 *   2. Token me kohë, i nënshkruar me HMAC: mesazhi pranohet vetëm 3 sekonda deri 2 orë
 *      pasi u hap formulari (robotët dërgojnë menjëherë ose përsërisin formularë të vjetër).
 *   3. Kufi: maksimumi 5 mesazhe në orë nga e njëjta adresë IP (ruhet vetëm hash-i i IP-së).
 *
 * Sekreti krijohet automatikisht në private/secret.php dhe nuk del kurrë në shfletues.
 */

declare(strict_types=1);
header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: no-store');
header('X-Content-Type-Options: nosniff');

const MIN_SEK = 3;
const MAKS_SEK = 7200;
const KUFI_NE_ORE = 5;

$private = dirname(__DIR__) . '/private';
if (!is_dir($private)) { @mkdir($private, 0750, true); }

function pergjigju(int $kodi, array $te_dhenat): void {
    http_response_code($kodi);
    echo json_encode($te_dhenat, JSON_UNESCAPED_UNICODE);
    exit;
}

function sekreti(string $private): string {
    $skedari = $private . '/secret.php';
    if (!is_file($skedari)) {
        $s = bin2hex(random_bytes(32));
        file_put_contents($skedari, "<?php return '" . $s . "';\n", LOCK_EX);
        @chmod($skedari, 0640);
    }
    return (string) require $skedari;
}

function token_i_ri(string $sekret): string {
    $koha = (string) time();
    return $koha . '.' . hash_hmac('sha256', $koha, $sekret);
}

function token_i_vlefshem(string $token, string $sekret): bool {
    $pjeset = explode('.', $token, 2);
    if (count($pjeset) !== 2 || !ctype_digit($pjeset[0])) return false;
    if (!hash_equals(hash_hmac('sha256', $pjeset[0], $sekret), $pjeset[1])) return false;
    $mosha = time() - (int) $pjeset[0];
    return $mosha >= MIN_SEK && $mosha <= MAKS_SEK;
}

$sekret = sekreti($private);

// ---- GET: token për formularin ----
if ($_SERVER['REQUEST_METHOD'] === 'GET') {
    pergjigju(200, ['token' => token_i_ri($sekret)]);
}
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    pergjigju(405, ['ok' => false, 'error' => 'method']);
}

// ---- Kontroll i origjinës: kërkesa duhet të vijë nga e njëjta faqe ----
$origjina = $_SERVER['HTTP_ORIGIN'] ?? '';
$hosti = preg_replace('/:\d+$/', '', $_SERVER['HTTP_HOST'] ?? '');
if ($origjina !== '' && parse_url($origjina, PHP_URL_HOST) !== $hosti) {
    pergjigju(403, ['ok' => false, 'error' => 'origin']);
}

// ---- 1. Fusha e fshehur: nëse është plotësuar, e injorojmë pa i treguar robotit ----
if (trim((string) ($_POST['website'] ?? '')) !== '') {
    pergjigju(200, ['ok' => true]);
}

// ---- 2. Token-i me kohë ----
if (!token_i_vlefshem((string) ($_POST['token'] ?? ''), $sekret)) {
    pergjigju(400, ['ok' => false, 'error' => 'token']);
}

// ---- 3. Kufiri i mesazheve për IP (ruajmë vetëm hash-in, jo IP-në) ----
$ip_hash = hash_hmac('sha256', $_SERVER['REMOTE_ADDR'] ?? '', $sekret);
$skedari_kufi = $private . '/kufiri.json';
$fh = fopen($skedari_kufi, 'c+');
if ($fh && flock($fh, LOCK_EX)) {
    $kufiri = json_decode((string) stream_get_contents($fh), true) ?: [];
    $tani = time();
    foreach ($kufiri as $h => $kohet) {                       // pastrojmë të dhënat më të vjetra se 1 orë
        $kufiri[$h] = array_values(array_filter($kohet, fn($k) => $k > $tani - 3600));
        if (!$kufiri[$h]) unset($kufiri[$h]);
    }
    if (count($kufiri[$ip_hash] ?? []) >= KUFI_NE_ORE) {
        flock($fh, LOCK_UN); fclose($fh);
        pergjigju(429, ['ok' => false, 'error' => 'rate']);
    }
    $kufiri[$ip_hash][] = $tani;
    ftruncate($fh, 0); rewind($fh);
    fwrite($fh, json_encode($kufiri));
    flock($fh, LOCK_UN); fclose($fh);
}

// ---- Validimi në server (asnjëherë mos u mbështet vetëm te validimi në shfletues) ----
$emri    = trim((string) ($_POST['name'] ?? ''));
$email   = trim((string) ($_POST['email'] ?? ''));
$tema    = (string) ($_POST['topic'] ?? 'other');
$mesazhi = trim((string) ($_POST['message'] ?? ''));
$gjuha   = (string) ($_POST['lang'] ?? 'en');
$pelqimi = (string) ($_POST['consent'] ?? '');

$gabime = [];
if ($emri === '' || mb_strlen($emri) > 80) $gabime[] = 'name';
if (!filter_var($email, FILTER_VALIDATE_EMAIL) || mb_strlen($email) > 120) $gabime[] = 'email';
if (!in_array($tema, ['suggest', 'fix', 'other'], true)) $gabime[] = 'topic';
if (mb_strlen($mesazhi) < 10 || mb_strlen($mesazhi) > 2000) $gabime[] = 'message';
if ($pelqimi !== '1') $gabime[] = 'consent';
if (!in_array($gjuha, ['en', 'it', 'sq'], true)) $gjuha = 'en';
// Shumë lidhje në mesazh = shenjë tipike spam-i
if (preg_match_all('~https?://~i', $mesazhi) > 3) $gabime[] = 'links';
if ($gabime) {
    pergjigju(422, ['ok' => false, 'error' => 'validation', 'fields' => $gabime]);
}

// ---- Ruajtja (CSV). Shmangim "CSV injection": vlerat që fillojnë me = + - @ ----
$pastro = function (string $v): string {
    $v = str_replace(["\r", "\0"], '', $v);
    return preg_match('/^[=+\-@]/', $v) ? "'" . $v : $v;
};
$rresht = [date('c'), $gjuha, $tema, $pastro($emri), $pastro($email), $pastro($mesazhi)];
$csv = $private . '/messages.csv';
$i_ri = !is_file($csv);
$fh = fopen($csv, 'a');
if (!$fh) pergjigju(500, ['ok' => false, 'error' => 'storage']);
flock($fh, LOCK_EX);
if ($i_ri) fputcsv($fh, ['data', 'gjuha', 'tema', 'emri', 'email', 'mesazhi']);
fputcsv($fh, $rresht);
flock($fh, LOCK_UN);
fclose($fh);

pergjigju(200, ['ok' => true]);
