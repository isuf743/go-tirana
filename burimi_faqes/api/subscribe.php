<?php
/**
 * GO TIRANA: regjistrimi në listën e emaileve.
 *
 * GET  ?token=1  -> token i nënshkruar me kohën aktuale
 * POST           -> validon dhe ruan emailin në private/subscribers.csv (pa dyfishime)
 *
 * Mbrojtja nga spam-i është e njëjtë me formularin e kontaktit:
 * fushë e fshehur, token HMAC (3 sekonda deri 2 orë), maksimumi 5 kërkesa në orë për IP (ruhet vetëm hash-i).
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
        file_put_contents($skedari, "<?php return '" . bin2hex(random_bytes(32)) . "';\n", LOCK_EX);
        @chmod($skedari, 0640);
    }
    return (string) require $skedari;
}

function token_i_vlefshem(string $token, string $sekret): bool {
    $pjeset = explode('.', $token, 2);
    if (count($pjeset) !== 2 || !ctype_digit($pjeset[0])) return false;
    if (!hash_equals(hash_hmac('sha256', $pjeset[0], $sekret), $pjeset[1])) return false;
    $mosha = time() - (int) $pjeset[0];
    return $mosha >= MIN_SEK && $mosha <= MAKS_SEK;
}

$sekret = sekreti($private);

if ($_SERVER['REQUEST_METHOD'] === 'GET') {
    $koha = (string) time();
    pergjigju(200, ['token' => $koha . '.' . hash_hmac('sha256', $koha, $sekret)]);
}
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    pergjigju(405, ['ok' => false, 'error' => 'method']);
}

// Kërkesa duhet të vijë nga e njëjta faqe
$origjina = $_SERVER['HTTP_ORIGIN'] ?? '';
$hosti = preg_replace('/:\d+$/', '', $_SERVER['HTTP_HOST'] ?? '');
if ($origjina !== '' && parse_url($origjina, PHP_URL_HOST) !== $hosti) {
    pergjigju(403, ['ok' => false, 'error' => 'origin']);
}

// Fusha e fshehur: robotët e plotësojnë; u themi "ok" pa ruajtur asgjë
if (trim((string) ($_POST['website'] ?? '')) !== '') {
    pergjigju(200, ['ok' => true]);
}
if (!token_i_vlefshem((string) ($_POST['token'] ?? ''), $sekret)) {
    pergjigju(400, ['ok' => false, 'error' => 'token']);
}

// Kufiri për IP (vetëm hash-i i IP-së ruhet)
$ip_hash = hash_hmac('sha256', $_SERVER['REMOTE_ADDR'] ?? '', $sekret);
$fh = fopen($private . '/kufiri_nl.json', 'c+');
if ($fh && flock($fh, LOCK_EX)) {
    $kufiri = json_decode((string) stream_get_contents($fh), true) ?: [];
    $tani = time();
    foreach ($kufiri as $h => $kohet) {
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

// Validimi në server
$email = strtolower(trim((string) ($_POST['email'] ?? '')));
$gjuha = (string) ($_POST['lang'] ?? 'en');
$gabime = [];
if (!filter_var($email, FILTER_VALIDATE_EMAIL) || mb_strlen($email) > 120) $gabime[] = 'email';
if ((string) ($_POST['consent'] ?? '') !== '1') $gabime[] = 'consent';
if (!in_array($gjuha, ['en', 'it', 'sq'], true)) $gjuha = 'en';
if ($gabime) pergjigju(422, ['ok' => false, 'error' => 'validation', 'fields' => $gabime]);

// Ruajtja pa dyfishime (kontrolli dhe shkrimi nën të njëjtën kyçje)
$csv = $private . '/subscribers.csv';
$fh = fopen($csv, 'c+');
if (!$fh || !flock($fh, LOCK_EX)) pergjigju(500, ['ok' => false, 'error' => 'storage']);
$ekziston = false;
$bosh = true;
while (($rr = fgetcsv($fh)) !== false) {
    $bosh = false;
    if (isset($rr[1]) && strtolower($rr[1]) === $email) { $ekziston = true; break; }
}
if (!$ekziston) {
    fseek($fh, 0, SEEK_END);
    if ($bosh) fputcsv($fh, ['data', 'email', 'gjuha']);
    fputcsv($fh, [date('c'), $email, $gjuha]);
}
flock($fh, LOCK_UN);
fclose($fh);
pergjigju(200, ['ok' => true]);
