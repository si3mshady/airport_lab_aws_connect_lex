provider "aws" {
  region = "us-east-1"
}

resource "aws_instance" "kops" {
  depends_on = [ aws_security_group.kops_sg ]
  ami           = "ami-0fc5d935ebf8bc3bc"
  instance_type = "t2.xlarge"
  key_name      = "sreuni"
  user_data     = <<-EOF
                #!/bin/bash

                sudo yum update -y
                sudo apt install awscli -y
                #!/bin/bash

                # Install kOps
                curl -LO https://github.com/kubernetes/kops/releases/download/$(curl -s https://api.github.com/repos/kubernetes/kops/releases/latest | grep tag_name | cut -d '"' -f 4)/kops-linux-amd64
                chmod +x kops-linux-amd64
                sudo mv kops-linux-amd64 /usr/local/bin/kops

                # Install kubectl
                curl -LO https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl
                chmod +x kubectl
                sudo mv kubectl /usr/local/bin/

                # Configure AWS CLI
                sudo apt-get update
                sudo apt-get install -y awscli

                # Create an S3 bucket for kOps state storage
                # # aws s3api create-bucket --bucket el-my-kops-state-store --region us-east-1

                # # Export environment variables for kOps
                export NAME=thecloudshepherd.sreuniversity.org
                export KOPS_STATE_STORE=s3://el-my-kops-state-store

                # # aws route53 create-hosted-zone --name trials.com --caller-reference myuniqueid
                # public hz required

                # # Create a Kubernetes cluster with kOps
                kops create cluster \
                --node-count 1 \
                --node-size t3.large \
                --zones us-east-1a \
                --name $NAME
               

                # Update the Kubernetes cluster with kOps
                # kops update cluster $NAME --yes

                # # Validate the Kubernetes cluster with kOps
                # kops validate cluster
                EOF

  iam_instance_profile = "${aws_iam_instance_profile.kops_profile.name}"
  vpc_security_group_ids      = ["${aws_security_group.kops_sg.id}"]

  tags = {
    Name = "kops-instance"
  }
}

resource "aws_iam_role" "kops_role" {
  name = "kops-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "kops_policy_attachment" {
  policy_arn = "arn:aws:iam::aws:policy/AdministratorAccess"
  role       = "${aws_iam_role.kops_role.name}"
}

resource "aws_iam_instance_profile" "kops_profile" {
  name = "kops-profile"

  role = "${aws_iam_role.kops_role.name}"
}

resource "aws_security_group" "kops_sg" {
  name_prefix = "kops-sg"

  ingress {
    from_port   = 0   # Allow traffic from all ports
    to_port     = 65535   # To all ports
    protocol    = "tcp"  # You can also specify "udp" if needed
    cidr_blocks = ["76.183.21.156/32"]
  }
  
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_eip" "kops_eip" {
  instance = "${aws_instance.kops.id}"
  
}

# s3://el-my-kops-state-store/k8s.sreuniversity.org/config ~.kube/config


# # kops export kubeconfig --all --state s3://el-my-kops-state-store/trials.com/config

# # export KUBECONFIG=https://el-my-kops-state-store.s3.amazonaws.com/trials.com/config

# s3://el-my-kops-state-store/k8s.sreuniversity.org/configs3