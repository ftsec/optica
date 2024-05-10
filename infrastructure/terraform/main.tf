

module "vpc" {
  source                    = "./modules/vpc"
  vpc_enable_dns_hostnames  = true
  vpc_enable_dns_support    = true
  cloudwatch_log_group_name = "/aws/cloudtrail/${var.cloudtrail_name}"
  flow_log_traffic_type     = "ALL"
  vpc_cidr_block            = "10.0.0.0/24"
  igw_name                  = "Optica-IGW"
  account_id                = var.account_id
  region                    = var.region
  cloudtrail_name           = "optica-trail"
}

module "terraform_state_kms_key" {
  source       = "./modules/kms"
  account_id   = var.account_id
  region       = var.region
  key_name     = "terraform_state_key"
  project_name = "optica"
}

module "dynmodb-table" {
  source      = "./modules/dynamodb"
  kms_key_arn = module.terraform_state_kms_key.key_arn
}

module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 20.0"
  cluster_name                    = var.cluster_name
  cluster_version                 = "1.29"
  create_kms_key                  = true
  cluster_endpoint_private_access = true
  #Normally would set this to false and access cluster via bastion host/Tightly controlled EC2 instance on cluster VPC network.
  cluster_endpoint_public_access  = false

  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnets_ids

  enable_irsa         = true
  authentication_mode = "API_AND_CONFIG_MAP"
  enable_cluster_creator_admin_permissions = true
  access_entries = {
    cluster_admin_access = {
      kubernetes_groups = []
      principal_arn     = module.eks_admins_iam_role.iam_role_arn

      policy_associations = {
        single = {
          policy_arn = "arn:aws:eks::aws:cluster-access-policy/AmazonEKSClusterAdminPolicy"
          access_scope = {
            type = "cluster"
          }
        }
      }
    }
  }



  eks_managed_node_group_defaults = {
    disk_size = 50
  }

  cluster_addons = {
    coredns = {
      most_recent = true
    }
    kube-proxy = {
      most_recent = true
    }
    vpc-cni = {
      most_recent = true
    }
  }

  eks_managed_node_groups = {
    general = {
      min_size     = 1
      max_size     = 10
      desired_size = 1

      instance_types = ["t3.large"]
      capacity_type  = "ON_DEMAND"

      labels = {
        "role" = "general"
      }
    }

    spot = {
      min_size     = 1
      max_size     = 10
      desired_size = 1

      instance_types = ["t3.large"]
      capacity_type  = "SPOT"

      labels = {
        "role" = "spot"
      }

      taints = [
        {
          key    = "market"
          value  = "spot"
          effect = "NO_SCHEDULE"
        }
      ]
    }
  }

  tags = {
    Environment = var.Environment
    Terraform   = "true"
  }
}


resource "aws_eks_addon" "pod_identity_agent_addon" {
  cluster_name = module.eks.cluster_name
  addon_name   = "eks-pod-identity-agent"
}
