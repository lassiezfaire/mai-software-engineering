workspace {
    name "Магазин"
    description "Лабораторная работа 01"

    model {

        properties { 
            structurizr.groupSeparator "/"
        }

        user = person "Пользователь интернет-магазина" {
            description "Пользователь интернет магазина, обладающий личным аккаунтом"
        }

        shop_owner = person "Владелец интернет-магазина" {
            description "Владелец интернет магазина, добавляющий в него товары"
        }

        online_shop = softwareSystem "Интернет-магазин" {
            description "Интернет-магазин, позволяющий пользователю просматривать товары и добавлять их в корзину, а владельцу - добавлять новые товары"

            api_app = container "API Application" {
                description "Предоставляет функционал интернет-магазина"
                technology "Python, FastAPI"
            }

            group "Слой данных" {
                user_db = container "User Database" {
                    description "Реляционная СУБД, содержащая информацию о пользователях"
                    technology "PostgreSQL 15"
                    tags "database"
                }

                user_cache = container "User Cache" {
                    description "Кеш пользовательских данных, хранимый для ускорения поиска информации о них"
                    technology "Redis"
                    tags "database"
                }

                shop_db = container "Shop Database" {
                    description "Документоориентированная СУБД, содержащая информацию о товарах магазина"
                    technology "MongoDB"
                    tags "database"
                }

                shopping_cart_db = container "Shopping Cart Database" {
                    description "Документоориентированная СУБД, содержащая информацию о содержимом корзин пользователей"
                    technology "MongoDB"
                    tags "database"
                }
            }

            api_app -> user_db "Получение/обновление данных о пользователе" "TCP:5432"
            api_app -> user_cache "Получение/обновление данных о пользователе" "TCP:6379"
            api_app -> shop_db "Получение/обвноление данных о товаре" "TCP:27017"
            api_app -> shopping_cart_db "Получение/обвноление данных о корзине пользователя" "TCP:27018"

            user -> api_app "Просмотр товаров и добавление их в корзину" "REST HTTP:8000"
            shop_owner -> api_app "Добавление товара в магазин" "REST HTTP:8000"
        }

        deploymentEnvironment "Production" {
            
            deploymentNode "node0" {
                description "Главная нода для запуска uvicorn и Redis"
                containerInstance api_app
                containerInstance user_cache
                properties {
                    "CPU" "2"
                    "RAM" "4Gb"
                    "HDD" "16Gb"
                }
            }

            deploymentNode "node1" {
                description "Нода для запуска PostgreSQL и MongoDB"
                containerInstance user_db
                containerInstance shop_db
                containerInstance shopping_cart_db
                properties {
                    "CPU" "2"
                    "RAM" "4Gb"
                    "HDD" "32Gb"
                }
            }

            deploymentNode "node2" {
                description "Нода для запуска PostgreSQL и MongoDB"
                containerInstance user_db
                containerInstance shop_db
                containerInstance shopping_cart_db
                properties {
                    "CPU" "2"
                    "RAM" "4Gb"
                    "HDD" "32Gb"
                }
            }

            deploymentNode "node3" {
                description "Нода для запуска PostgreSQL и MongoDB"
                containerInstance user_db
                containerInstance shop_db
                containerInstance shopping_cart_db
                properties {
                    "CPU" "2"
                    "RAM" "4Gb"
                    "HDD" "32Gb"
                }
            }

            deploymentNode "Databases Server" {

                deploymentNode "Database Server 1" {
                    containerInstance user_db
                    instances 3
                }

                deploymentNode "Database Server 2" {
                    containerInstance user_cache
                    instances 1
                }

                deploymentNode "Database Server 3" {
                    containerInstance shop_db
                    instances 3
                }

                deploymentNode "Database Server 4" {
                    containerInstance shopping_cart_db
                    instances 3
                }
            }
        }
    }

    views {
        themes default

        properties { 
            structurizr.tooltips true
        }

        !script groovy {
            workspace.views.createDefaultViews()
            workspace.views.views.findAll { it instanceof
            com.structurizr.view.ModelView }.each { it.enableAutomaticLayout() }
        }

        systemContext online_shop "systemContext" {
            include *
            autoLayout
        }

        container online_shop "container" {
            include *
            autoLayout
        }

        deployment online_shop "Production" "deployment" {
            include *
            autoLayout
        }

        styles {
            element "database" {
                shape cylinder
            }
        }
    }
}