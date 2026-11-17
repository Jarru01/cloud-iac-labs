# AWS lab 2 — bastion host and VPC peering

| Template | Creates |
|---|---|
| `basic-network.yaml` | Primary VPC `10.20.0.0/16`: public and private subnets in 3 AZs, internet gateway, one NAT gateway per AZ. Exports VPC, subnet and route table IDs. |
| `bastion.yaml` | Bastion host in public subnet A (SSH only from `AdminCidr`) and a private instance reachable only through it. |
| `secondary-vpc.yaml` | Secondary VPC `10.222.0.0/16` with one private instance, a VPC peering connection to the primary VPC, and routes on **both** sides of the peering. |

## Deploy

```bash
aws cloudformation deploy --stack-name basic-network --template-file basic-network.yaml

aws cloudformation deploy --stack-name bastion --template-file bastion.yaml \
  --parameter-overrides AdminCidr=203.0.113.10/32 IamInstanceProfileName=<profile>

aws cloudformation deploy --stack-name secondary-vpc --template-file secondary-vpc.yaml \
  --parameter-overrides IamInstanceProfileName=<profile>
```

```
            Internet
               │
     ┌─────────┴──────────┐            VPC peering            ┌──────────────────────┐
     │  Primary VPC        │◄──────────────────────────────────►│  Secondary VPC        │
     │  10.20.0.0/16       │                                    │  10.222.0.0/16        │
     │                     │                                    │                       │
     │  public subnet A    │                                    │  private subnet       │
     │   └ BastionA ──ssh──┼──► PrivateInstance (private A)     │   └ PrivateInstance_  │
     │                     │                                    │      secondaryVPC     │
     └─────────────────────┘                                    └───────────────────────┘
```

## Troubleshooting notes

These are the problems hit while building the lab, and how the templates
now handle them.

1. **EC2 Instance Connect to the bastion failed.** The bastion security group
   allowed SSH only from one admin address, but browser-based EC2 Instance
   Connect connects from the AWS-owned `EC2_INSTANCE_CONNECT` IP range for the
   region. Fix: connect with a normal SSH client from `AdminCidr`, or use
   Session Manager (the instances get an SSM instance profile). Opening port
   22 to `0.0.0.0/0` works too, but only as a temporary measure.

2. **Bastion could not ping the private instance in the primary VPC.** The
   private instance's security group did not allow ICMP from the VPC CIDR.
   Fix: ICMP is allowed from the primary VPC CIDR (and the peered VPC), and
   the bastion's security group allows ICMP egress to both.

3. **Bastion could not ping the instance in the secondary VPC**, even with
   ICMP allowed. Security groups were fine, but the bastion's subnet uses the
   *public* route table, which had no route to `10.222.0.0/16`. The first fix
   was to hard-code the peering ID (`pcx-…`) into `basic-network.yaml` and
   update the stack after the peering existed.

   The templates now avoid that two-step manual edit: `basic-network.yaml`
   exports its public and private route table IDs, and `secondary-vpc.yaml`
   adds the routes to them right after creating the peering connection.

Result: bastion → private instance (primary VPC) ✅ and bastion → private
instance (secondary VPC) ✅.
