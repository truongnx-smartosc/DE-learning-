# Cấu hình provider GCP
provider "google" {
  credentials = file("./top-broker-458809-c0-78521e6b7e6f.json") # Đường dẫn tới file JSON của bạn
  project     = "top-broker-458809-c0"     # Thay bằng ID dự án của bạn
  region      = "us-central1"
}

# Tạo VM
resource "google_compute_instance" "vm_instance" {
  name         = "terraform-vm" 
  machine_type = "e2-medium"   # Loại máy ảo (cấu hình trung bình)
  zone         = "us-central1-a"

  boot_disk {
    initialize_params {
      image = "projects/debian-cloud/global/images/family/debian-12"
    }
  }

  network_interface {
    network = "default"

    access_config {
      // Cấp IP công cộng
    }
  }

  # Tùy chọn: Thêm SSH keys
  metadata = {
    ssh-keys = "truongnx1:ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIM1DNeZb+r0vjTGHphtwwnLz8GgjpTC0jLaZsTDMvW3d nguyenxuantruong@truongnguyen.local"
  }
}