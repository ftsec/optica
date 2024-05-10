
#tfsec:ignore:aws-ec2-no-public-ip-subnet
resource "aws_subnet" "public_subnet_1" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.0.0/26"
  availability_zone       = "us-west-2a"
  map_public_ip_on_launch = true
  tags = {
    Name                                            = "public-us-west-1a"
    "kubernetes.io/cluster/${var.eks_cluster_name}" = "shared"
    "kubernetes.io/role/elb"                        = "1"
    "tier"                                          = "public"
  }
}
#tfsec:ignore:aws-ec2-no-public-ip-subnet
resource "aws_subnet" "public_subnet_2" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.0.64/26"
  availability_zone = "us-west-2b"
  map_public_ip_on_launch = true
  tags = {
    Name                                            = "public-us-west-1b"
    "kubernetes.io/cluster/${var.eks_cluster_name}" = "shared"
    "kubernetes.io/role/elb"                        = "1"
    "tier"                                          = "public"
  }
}

resource "aws_subnet" "private_subnet_1" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.0.128/26"
  availability_zone = "us-west-2a"
  tags = {
    Name                                            = "private-us-west-1a"
    "kubernetes.io/role/elb"                        = "1"
    "kubernetes.io/cluster/${var.eks_cluster_name}" = "shared"
    "tier"                                          = "private"
  }
}

resource "aws_subnet" "private_subnet_2" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.0.192/26"
  availability_zone = "us-west-2b"
  tags = {
    Name                                            = "private-us-west-1b"
    "kubernetes.io/role/elb"                        = "1"
    "kubernetes.io/cluster/${var.eks_cluster_name}" = "shared"
    "tier"                                          = "private"
  }
}
