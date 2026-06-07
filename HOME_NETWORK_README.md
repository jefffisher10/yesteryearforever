# Home network setup — reference

*How it's all put together. Not a how-to — a map, for when memory fails.*
*Configured: June 7, 2026*

---

## The short version

Three things got built today, and they stack on top of each other:

1. **The router** runs custom firmware (FreshTomato) instead of stock Netgear — this is the foundation that makes the other two possible.
2. **Remote access** is a private VPN (WireGuard) *into* the home network — no admin pages exposed to the internet.
3. **DNS auto-update** keeps the domain names pointed at home as the ISP changes the public IP — so the website and the VPN never silently break.

If you only remember one sentence: *the router is FreshTomato, you get in from outside via the WireGuard app on your phone, and a script on botpi keeps GoDaddy pointed home automatically.*

---

## 1. The router

- **Hardware:** Netgear Nighthawk R7000
- **Firmware:** FreshTomato 2026.2, K26ARM, AIO build (replaced stock Netgear)
- **Router name:** FisherTomato
- **Admin page:** http://192.168.1.1 (plain HTTP, only reachable from inside the network or through the VPN)
- **WAN:** DHCP from the ISP, no login / no PPPoE
- **Why FreshTomato:** stock Netgear removed remote management and phones home with data; FreshTomato restores full control (static IPs, port forwarding, VPN) and is private.
- **Undo button:** the stock config backup `NETGEAR_R7000.cfg` is saved. Re-flashing stock Netgear firmware + restoring that file returns the router to how it was before.

The R7000 is very hard to brick — it has a built-in TFTP recovery mode if a future firmware change ever goes wrong.

---

## 2. The network — who lives where

Key devices have fixed addresses so nothing drifts:

| Device | Address | How the address is set |
|---|---|---|
| Router (FisherTomato) | 192.168.1.1 | — |
| botpi (hosts the website) | 192.168.1.33 | static, set on the Pi itself (NetworkManager) |
| MOUND Pi (sensor observatory) | its own static | set on the Pi itself |
| FreeNAS server | 192.168.1.222 | set on the NAS itself |

**Port forwarding:** ports **80** and **443** → **192.168.1.33** (botpi). This is what lets the outside world reach the website. It's the only forward; everything else stays inside.

---

## 3. Remote access — WireGuard VPN

Instead of exposing the router's admin page to the internet (risky, and what Netgear killed), there's a private encrypted tunnel. Nothing is visible from outside; the only way in is with a key held on your devices.

**Where it runs:** on the router itself (FreshTomato → VPN Tunneling → WireGuard → `wg0`), in Hub-and-Spoke mode. The router is the hub; your devices are spokes.

**The numbers:**
- Tunnel subnet: `10.22.0.0/24`
- Router (server) end: `10.22.0.1`
- Phone (peer "MyPixel"): `10.22.0.2`
- Listen port: UDP `51820`
- LAN access + firewall opening are handled automatically by Hub/Spoke mode (no extra toggles).

**On the phone:** the WireGuard app holds a config called *MyPixel*. Its key settings:
- **Endpoint:** `yesteryearforever.xyz:51820` (a domain, not a fixed IP — so it follows the home IP)
- **AllowedIPs:** `192.168.1.0/24, 10.22.0.0/24` (split tunnel — only home-network traffic goes through the tunnel; normal phone traffic stays normal)

**How to actually use it:** away from home, flip the WireGuard toggle on in the phone app. Then reach anything at its normal address — `192.168.1.1` for the router admin, `192.168.1.33` for botpi, `192.168.1.222` for the NAS. Turn it off when home (no need to run it on the home Wi-Fi).

**Security note:** the WireGuard config file (`MyPixel.conf`) contains a private key — anyone with that file can get in. Keep it off shared inboxes/cloud folders; the phone's app stores it securely. To add another device later, generate a *new* peer on the router (don't reuse the phone's).

---

## 4. DNS auto-update — the glue

**The problem it solves:** both domains are registered at GoDaddy, and their root A records must point at the home public IP. But the ISP's IP is dynamic — it changes every few months without warning. When it changes, both the website *and* the WireGuard endpoint go dark until the record is fixed. This automates that fix.

**Domains (both at GoDaddy, same account):**
- yesteryearforever.xyz
- yesteryearforever.com

**The mechanism:** a script on botpi runs on a schedule, checks the current public IP, compares it to each domain's GoDaddy A record, and updates GoDaddy (via its API) *only when the IP has actually changed*.

| Thing | Where |
|---|---|
| Script | `/home/botpi/godaddy_ddns.py` |
| Log (writes only on change or error) | `/home/botpi/ddns.log` |
| Schedule | cron, every 15 min: `*/15 * * * * /usr/bin/python3 /home/botpi/godaddy_ddns.py` |
| Credentials | a GoDaddy **Production** API key + secret live inside the script (file is `chmod 700`) |
| Public-IP source | `https://api.ipify.org` |

A normal run where the IP hasn't changed does nothing and writes nothing — silence is success. A log entry appears only when it updates a record or hits an error.

**Gotcha for later:** if the script runs clean but a record won't update, check whether GoDaddy's **Domain Protection** is enabled on that domain — it can silently block API edits.

---

## How it all fits together

```
   GoDaddy DNS (.xyz + .com root A records)
        ^                         |
        | auto-updated by         | resolve to
        | botpi script every      | home public IP
        | 15 min                  v
   [ botpi cron ]          Home public IP  <-- changes occasionally (ISP)
                                  |
                                  v
                           [ R7000 / FreshTomato ]
                          /          |            \
              80/443 forward    WireGuard wg0    (LAN gateway)
                    |            UDP 51820              |
                    v                |                  |
              botpi :33         phone "MyPixel"    MOUND, NAS, etc.
            (serves website)    (tunnel in from
                                 anywhere)
```

- **Website path:** domain → home IP → router forwards 80/443 → botpi serves the site.
- **Remote-access path:** phone VPN toggle → tunnel to the router → reach the whole LAN.
- **The DDNS script** is the piece that keeps the domain names pointed home as the IP drifts, which is what keeps *both* of the above working unattended.

---

## If something breaks — where to look first

- **Website unreachable from outside:** compare the home public IP to the GoDaddy A records; check `ddns.log`; confirm botpi is up and the 80/443 forward still exists in the router.
- **Can't VPN in from outside:** confirm `yesteryearforever.xyz` currently resolves to the real home IP (DDNS may be lagging a recent change); confirm the WireGuard tunnel shows **Up** on the router.
- **DDNS not updating:** read `ddns.log` for errors; check the GoDaddy API key is still valid; check Domain Protection isn't silently blocking edits.
- **Router admin or menu acting strange after changes:** FreshTomato caches aggressively in the browser — hard-refresh (Ctrl+Shift+R) or open in an incognito window. This fixed both a login loop and a missing-menu scare during setup.
- **Locked out of the router entirely:** connect by wired Ethernet to `192.168.1.1`; if needed, TFTP recovery mode restores it (it's hard to brick).

---

## Companion documents

- **R7000 FreshTomato prep sheet** — the pre-flash settings record.
- **R7000 FreshTomato flash guide** — the full step-by-step flashing procedure, if the firmware ever needs redoing.

*Built the slow, hands-on way — which is the whole point.*
