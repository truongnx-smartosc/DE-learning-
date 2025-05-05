terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~>3.0"
    }
  }
  required_version = ">= 1.2.0"
}

provider "azurerm" {
  features {}
}

# 1. Resource Group
resource "azurerm_resource_group" "rg" {
  name     = "myResourceGroup"
  location = "East US"  # chọn vùng phù hợp
}

# 2. Virtual Network
resource "azurerm_virtual_network" "vnet" {
  name                = "myVNet"
  address_space       = ["10.0.0.0/16"]
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
}

# 3. Subnet
resource "azurerm_subnet" "subnet" {
  name                 = "mySubnet"
  resource_group_name  = azurerm_resource_group.rg.name
  virtual_network_name = azurerm_virtual_network.vnet.name
  address_prefixes     = ["10.0.1.0/24"]
}

# 4. Public IP
resource "azurerm_public_ip" "public_ip" {
  name                = "myPublicIP"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  allocation_method   = "Static"
  sku                 = "Standard"
}

# 5. Network Interface
resource "azurerm_network_interface" "nic" {
  name                = "myNIC"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name

  ip_configuration {
    name                          = "ipconfig"
    subnet_id                     = azurerm_subnet.subnet.id
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id          = azurerm_public_ip.public_ip.id
  }
}

# 6. Container Instance for your app
resource "azurerm_container_group" "app_container" {
  name                = "myContainerGroup"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  ip_address_type     = "public"
  dns_name_label      = "myapp-${random_string.suffix.result}"

  container {
    name   = "myapp"
    image  = "truongyuchi/docker-terra-app-web:latest"  # Docker image của bạn
    cpu    = "0.5"
    memory = "1.5"

    ports {
      port     = 80
      protocol = "TCP"
    }
  }

  os_type = "Linux"

  # Cấu hình để mở port
  ip_address {
    ports = [
      {
        port     = 80
        protocol = "TCP"
      }
    ]
  }

  network_profile_id = azurerm_network_interface.nic.id
}

# 7. Tạo Postgres Database (tùy chọn nếu dùng dịch vụ quản lý)
# - Bạn có thể dùng Azure Database for PostgreSQL nếu muốn, hoặc dùng container PostgreSQL
#   - Ở ví dụ này, hướng dẫn ta dùng container PostgreSQL khác vì dễ quản lý

# Ở đây, bạn có thể tự kéo về container PostgreSQL hoặc tạo database riêng
# hoặc dùng dịch vụ Azure Database for PostgreSQL (khác khai báo này)

# Mục tiêu: kết nối app container với database đúng cấu hình