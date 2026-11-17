# Cloud Technologies â€” IaC Labs

[![lint](https://github.com/Jarru01/cloud-iac-labs/actions/workflows/lint.yml/badge.svg)](https://github.com/Jarru01/cloud-iac-labs/actions/workflows/lint.yml)

Infrastructure-as-Code exercises from the *Virtualization and Cloud
Technologies* university course: AWS CloudFormation, OpenStack Heat, and
Terraform/OpenTofu templates.

## ðŸ“‚ Contents

| Folder | Tool | What it builds |
|---|---|---|
| [`aws1/`](aws1/) | CloudFormation | Base VPC â€” public and private subnets in 3 AZs, internet gateway, NAT gateway per AZ |
| [`aws2/`](aws2/) | CloudFormation | Bastion host, private instances, VPC peering with routes on both sides ([notes](aws2/README.md)) |
| [`aws3/`](aws3/) | CloudFormation | EC2 key pair, security groups and private web servers; Application Load Balancer in front of an Auto Scaling group |
| [`aws5/`](aws5/) | CloudFormation | CloudWatch CPU alarms driving scaling policies with SNS email alerts; private, encrypted, versioned S3 bucket |
| [`openstack1/`](openstack1/) | Heat | Basic topologies, including a Linux VM acting as router/NAT ([notes](openstack1/README.md)) |
| [`openstack2/`](openstack2/) | Heat | Ten advanced templates â€” routers, fixed IPs, conditions, key pairs, resource groups ([notes](openstack2/README.md)) |
| [`terraform/`](terraform/) | Terraform / OpenTofu | Single OpenStack instance, credentials from `clouds.yaml` or `OS_*` variables |
| [`k8s/`](k8s/) | â€” | Kubernetes study notes |

## ðŸš€ Deploying

**AWS** â€” stacks reference each other through exports, so deploy the network
first. The `aws5` alarms attach to the Auto Scaling group from `aws3`.

```bash
aws cloudformation deploy --stack-name basic-network --template-file aws3/basic-network.yaml
aws cloudformation deploy --stack-name ec2 --template-file aws3/ec2_asg.yaml \
  --parameter-overrides OurPublicIp=203.0.113.10/32 IamInstanceProfileName=<profile>
aws cloudformation deploy --stack-name alarms --template-file aws5/cloudwatch.yaml \
  --parameter-overrides EC2StackName=ec2 NotificationEmail=you@example.com
```

AMIs are resolved from the public SSM parameter for the latest Amazon Linux
2023 image, so the templates work in any region without editing.

**OpenStack Heat**

```bash
openstack stack create -t openstack2/task10.yml --parameter vm_count=3 demo
```

**Terraform / OpenTofu**

```bash
export OS_CLOUD=mycloud        # entry in clouds.yaml, or source an openrc file
cd terraform
terraform init && terraform apply   # or: tofu init && tofu apply
```

## ðŸ” Credentials

No credentials are stored in this repository.

- **AWS:** deploy with your own CLI profile. Account-specific values (IAM
  instance profile name, notification email, source IP) are stack parameters.
- **OpenStack / Terraform:** credentials come from a `clouds.yaml` entry
  (`OS_CLOUD`) or from the `OS_*` variables of an OpenStack RC file.

## âœ… Checks

Every push runs [`lint.yml`](.github/workflows/lint.yml):

- `cfn-lint` on all CloudFormation templates
- `terraform fmt -check` and `terraform validate`
- an offline reference check for the Heat templates
  ([`check_heat.py`](.github/scripts/check_heat.py)): YAML syntax and every
  `get_param` / `get_resource` / `get_attr` / `depends_on` target

## ðŸ™ Credits

Some templates build on starter material provided by the course instructors.
`aws3/basic-network.yaml` and `aws3/ec2_asg.yaml` are course-provided
templates (the latter includes the sample web application from the lab).
They are adapted with lab parameters, and `ec2_asg.yaml` was updated from
a launch configuration to a launch template with IMDSv2 and an SSM-based AMI
lookup. The other templates were written or substantially reworked as part of
the exercises.

## âš ï¸ Scope

These are educational lab templates, not production-ready infrastructure.

## ðŸ“„ License

[MIT](LICENSE), for my own work in this repository. Course-provided material
listed under *Credits* remains with its authors.
