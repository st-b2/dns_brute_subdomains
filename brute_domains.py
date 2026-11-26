import sys
import dns.resolver
from concurrent.futures import ThreadPoolExecutor, as_completed

def wordlist(filename):
    try:
        with open(filename, 'r') as f:
            return [line.strip() for line in f.readlines()]
    except FileNotFoundError:
        print(f'[-] Wordlist file "{filename}" not found')
        sys.exit(1)

def resolve_subdomain(fqdn, resolver):
    try:
        answers = resolver.resolve(fqdn, 'A')
        return [(fqdn, a.address) for a in answers]
    except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer):
        return None
    except Exception as e:
        print(f'[-] Error {fqdn}: {e}')
        return None

def worker(sub, domain, wordlist):
    fqdn = f'{sub}.{domain}'
    return resolve_subdomain(fqdn, wordlist)

def brute_domains(domain, wordlist_file, threads=20):
    subdomains = wordlist(wordlist_file)
    print(f'[-] Loaded {len(subdomains)} names for testing. Threads: {threads}')
    print(f'[-] Target domains: {domain}\n')


    resolver = dns.resolver.Resolver()
    resolver.timeout = 1.5
    resolver.lifetime = 3.0
    founds = []

    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = {executor.submit(worker, sub, domain, resolver): sub for sub in subdomains}
        for future in as_completed(futures):
            result = future.result()
            if result:
                for fqdn, ip in result:
                    print(f'[+] {fqdn}  ->  {ip}')
                    founds.append((fqdn, ip))

    print(f'\n[!] Founded {len(founds)} names for testing')
    return founds


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(f'[!] Usage: {sys.argv[0]} <domain> <wordlist_file>')
        sys.exit(1)

    domain = sys.argv[1]
    wordlist_file = sys.argv[2]
    brute_domains(domain, wordlist_file)