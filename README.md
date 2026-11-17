# Cloud Technologies — IaC Labs

Infrastructure-as-Code exercises from the *Virtualization and Cloud
Technologies* university course: AWS CloudFormation, OpenStack HEAT, and
Terraform/OpenTofu templates.

## 📂 Contents

| Folder | Topic |
|---|---|
| [`aws1/`](aws1/) | AWS basics, automation tools, versioning |
| [`aws2/`](aws2/) | VPC networking — SG/NACL, VPC peering, S2S VPN, Direct Connect, PrivateLink, Transit Gateway |
| [`aws3/`](aws3/) | EC2 instances, autoscaling groups & load balancing |
| `aws4` *(not committed)* | Lambda, Step Functions, API Gateway, containers |
| [`aws5/`](aws5/) | CloudFormation — S3, CloudWatch alarms (deployed on top of the `aws3/` network and ASG stacks) |
| [`openstack1/`](openstack1/) | Basic HEAT templates for OpenStack |
| [`openstack2/`](openstack2/) | Advanced HEAT templates |
| [`terraform/`](terraform/) | Basic Terraform/**OpenTofu** script |
| [`k8s/`](k8s/) | Kubernetes study summary |

## 🔐 Credentials

No credentials are stored in this repository.

- **AWS:** deploy with your own CLI profile. Account-specific values (IAM
  instance profile name, notification email, source IP) are stack parameters.
- **OpenStack / Terraform:** the provider reads credentials from a
  `clouds.yaml` entry (`OS_CLOUD`) or from the `OS_*` variables of an
  OpenStack RC file.

## 🙏 Credits

Some templates build on starter material provided by the course instructors:
`aws3/basic-network.yaml` and `aws3/ec2_asg.yaml` are course-provided templates
(the latter includes the sample web application setup from the lab), adapted
only with lab-specific parameters. The other templates were written or
substantially reworked as part of the exercises.

## ⚠️ Scope

These are educational lab templates, not production-ready infrastructure.
