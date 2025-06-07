# Project1_IAM

# 🔐 Project 1: IAM Least Privilege with Tag-Based S3 Access and Real-Time Monitoring

## 🎯 Objective

This project simulates a real-world AWS cloud security scenario focused on enforcing **least privilege access** to S3 resources using **tag-based IAM policies**, while implementing **defense-in-depth** with IP restrictions, public access blocking, and **real-time access monitoring** using CloudTrail, CloudWatch, and SNS.

---

## 🧱 Architecture Diagram

![Architecture Diagram](./architecture-diagram.png)

---

## 🛠️ AWS Services Used

- AWS IAM  
- Amazon S3 (with server-side encryption and tags)  
- AWS CloudTrail (with S3 Data Events)  
- Amazon CloudWatch Logs  
- CloudWatch Metric Filters and Alarms  
- Amazon SNS (email notification)

---

## 🔑 Key Features

- ✅ IAM policy enforces tag-based access control (`s3:ResourceTag`)
- ✅ Bucket encrypted with server-side encryption (SSE)
- ✅ Bucket public access completely blocked
- ✅ S3 `GetObject` actions logged with CloudTrail
- ✅ CloudWatch alarm sends email alert via SNS on access events

---

## 🧪 Test Scenarios

| Scenario | Result |
|----------|--------|
| IAM user accesses object with matching tag | ✅ Allowed |
| IAM user accesses object with unmatched tag | ❌ Denied |
| IAM user accesses from disallowed IP address | ❌ Denied |
| IAM user performs `GetObject` → CloudWatch detects & alerts | ✅ Alert triggered |

---

## 📜 IAM Policy (Tag-Based Access)

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowS3GetObjectWithTagCondition",
      "Effect": "Allow",
      "Action": ["s3:GetObject"],
      "Resource": "arn:aws:s3:::confidential-data-bucket/*",
      "Condition": {
        "StringEquals": {
          "s3:ResourceTag/project": "confidential"
        }
      }
    }
  ]
}
