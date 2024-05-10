resource "aws_nat_gateway" "nat_gw1" {
  allocation_id = aws_eip.nat1.id
  subnet_id     = aws_subnet.public_subnet_1.id
  tags = {
    Name = "gw NAT 1"
  }
}

resource "aws_nat_gateway" "nat_gw2" {
  allocation_id = aws_eip.nat2.id
  subnet_id     = aws_subnet.public_subnet_2.id
  tags = {
    Name = "gw NAT 2"
  }
}

resource "aws_eip" "nat1" {
  depends_on = [aws_internet_gateway.main]
}

resource "aws_eip" "nat2" {
  depends_on = [aws_internet_gateway.main]
}