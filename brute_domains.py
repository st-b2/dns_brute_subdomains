import sys
import dns.resolver

def wordlist(filename):
    try:
        with open(filename, 'r') as f:
            return [line.strip() for line in f.readlines()]
    except FileNotFoundError:
        print(f'[-] Wordlist file "{filename}" not found')
        sys.exit(1)


def brute_domains(domain, wordlist_file):
    subdomains = wordlist(wordlist_file)
    print(f'[-] Loaded {len(subdomains)} names for testing')
    print(f'[-] Target domains: {domain}\n')

    founds = []
    resolver = dns.resolver.Resolver()
    resolver.timeout = 1.5
    resolver.lifetime = 3.0

    for sub in subdomains:
        qdn = f'{sub}.{domain}'
        try:
            answers = resolver.resolve(qdn, 'A')
            for answer in answers:
                ip = answer.address
                print(f'[+] Found {qdn} -> {ip}')
                founds.append(ip)
        except dns.resolver.NXDOMAIN:
            pass
        except dns.resolver.NoAnswer:
            pass
        except dns.resolver.Timeout:
            print(f'[-] Timeout for {qdn}')
        except dns.resolver.NoNameservers:
            print(f'[-] No Nameservers for {qdn}')
        except Exception:
            print(f'[-] Unknown error for {qdn}')

    print(f'\n[!] Founded {len(founds)} names for testing')
    return founds


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(f'[!] Usage: {sys.argv[0]} <domain> <wordlist_file>')
        sys.exit(1)

    domain = sys.argv[1]
    wordlist_file = sys.argv[2]
    brute_domains(domain, wordlist_file)