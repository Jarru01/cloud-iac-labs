# OpenStack Heat — basic templates

Deploy with the OpenStack CLI (requires `python-heatclient`):

```bash
openstack stack create -t task1.yml task1
openstack stack output show task1 --all
```

Image, flavor and network names default to the values of the course cloud
and can be overridden with `--parameter key=value`.

---

## Task 1 — `task1.yml`
**Two VMs on the same external network**

Creates a security group (ICMP + SSH), two Neutron ports on `ext-net-154`
and two VMs (`vm1`, `vm2`), each attached to its own port. There is no
internal network; both VMs sit directly on the external network.

```
┌─────────────────────────────────────┐
│          ext-net-154                │
│                                     │
│   ┌──────────┐    ┌──────────┐      │
│   │   vm1    │    │   vm2    │      │
│   │ (cirros) │    │ (cirros) │      │
│   └──────────┘    └──────────┘      │
│      port1           port2          │
└─────────────────────────────────────┘

Security group: ICMP + TCP/22
```

---

## Task 2 — `task2.yml`
**VM router with an internal VM behind it**

Creates the internal network `net-is1` (subnet `192.168.50.0/24`), a
security group (ICMP + SSH) and two VMs. `vm-router` has one interface on
the external network and one on the internal network and enables IP
forwarding at boot; `vm-internal` is connected only to the internal network.

```
                  ext-net-154
                       │
              ┌────────┴────────┐
              │    vm-router    │
              │    (cirros)     │
              │  IP forwarding  │
              └────────┬────────┘
                       │
          ┌────────────────────────┐
          │  net-is1               │
          │  192.168.50.0/24       │
          │                        │
          │  ┌─────────────────┐   │
          │  │   vm-internal   │   │
          │  │    (cirros)     │   │
          │  └─────────────────┘   │
          └────────────────────────┘

Security group: ICMP + TCP/22
```

---

## Task 3 — `task3.yml`
**Router/NAT VM and a web server behind it**

Creates the internal network `net-is2` (subnet `10.0.1.0/24`, no Neutron
gateway) and two Debian VMs:

- `router-vm` is dual-homed. Its internal port has a fixed address
  (`10.0.1.254`) and **port security disabled**, because Neutron's
  anti-spoofing rules would otherwise drop packets it forwards for other
  hosts. At boot it enables IP forwarding and NATs (masquerades) traffic out
  of whichever interface holds its default route.
- `web-vm` lives only on the internal network. Its user data points the
  default route at the router VM, waits until the internet is reachable,
  then installs Apache.

```
  Internet
     │
  ext-net-154
     │
┌────┴──────────────┐
│    router-vm      │
│  (debian-12-kis)  │
│  ip_forward + NAT │
└────┬──────────────┘
     │ 10.0.1.254
┌────────────────────────────┐
│  net-is2  (10.0.1.0/24)    │
│                            │
│  ┌──────────────────────┐  │
│  │       web-vm         │  │
│  │   (debian-12-kis)    │  │
│  │   Apache2 (HTTP:80)  │  │
│  └──────────────────────┘  │
└────────────────────────────┘

router-vm SG:  SSH from trusted_cidr (default 158.193.0.0/16), ICMP
web-vm SG:     SSH from trusted_cidr and from 10.0.1.0/24, HTTP, ICMP
```

The web server is reachable from inside `net-is2` (e.g. via SSH to the
router VM). Publishing it to the outside would need a DNAT rule on the
router VM or a floating IP.
