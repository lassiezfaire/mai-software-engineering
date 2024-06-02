workspace {
    name "Магазин"
    description "Лабораторная работа 01"

    model {
        user = person "Пользователь интернет-магазина" {
            description "Пользователь интернет магазина, обладающий личным аккаунтом"
        }

        online_shop = softwareSystem "Интернет-магазин" {
            description "Интернет-магазин, позволяющий пользователям просматривать и добавлять новые товары, а также добавлять их в корзину"

            front_service = container "UI Application" {
                description "Предоставляет пользователям возможность взаимодействия с магазином через браузер"
                technology "HTML/CSS/JS"
            }

            api_gateway = container "API Gateway" {
                description "Проксирует запросы к сервисам, реализует Circuit Breaker"
                technology "Python/FastAPI"
            }

            user_service = container "User Service" {
                description "Микросервис для работы с данными пользователей и выдачи JWT-токенов"
                technology "Python/FastAPI"
            }

            showcase_service = container "Showcase Service" {
                description "Микросервис для работы с витриной (т.е. с данными товаров)"
                technology "Python/FastAPI"
            }

            cart_service = container "Cart Service" {
                description "Микросервис для работы с корзиной пользователя"
                technology "Python/FastAPI"
            }

            group "Слой данных" {
                user_db = container "User and Cart Database" {
                    description "Реляционная СУБД, содержащая информацию о пользователях и их корзинах"
                    technology "PostgreSQL"
                    tags "database"
                }

                user_cache = container "User Cache Database" {
                    description "Кеш данных, хранимый для ускорения поиска информации о пользователях"
                    technology "Redis"
                    tags "database"
                }

                showcase_db = container "Showcase Database" {
                    description "Документоориентированная СУБД, содержащая информацию о товарах"
                    technology "MongoDB"
                    tags "database"
                }
            }
            
            front_service -> api_gateway "Перенаправление пользовательских запросов в микросервисы" "TCP:8080"

            api_gateway -> user_service "Получение запроса о работе с данными пользователей или получении JWT-токена" "TCP:8000"
            api_gateway -> showcase_service "Получение запроса о работе с витриной (данными товаров)" "TCP:8001"
            api_gateway -> cart_service "Получение запроса о работе с данными пользовательских корзин" "TCP:8002"

            user_service -> user_db "Манипуляции с данными пользователей" "TCP:5432"
            user_service -> user_cache "Манипуляции с данными пользователей" "TCP:6379"
            showcase_service -> showcase_db "Манипуляции с данными товаров" "TCP:27017"
            cart_service -> user_db "Манипуляции с данными корзин пользователей" "TCP:5432"
        }

        user -> front_service "Регистрация/авторизация/добавление товара в корзину и т.п." "REST HTTP:8000"

        deploymentEnvironment "Production" {
            
            deploymentNode "node0" {
                description "Нода для запуска фронт-энд приложения"
                containerInstance front_service
                properties {
                    "RAM" "4Gb"
                    "HDD" "16Gb"
                }
            }

            deploymentNode "node1" {
                description "Нода для запуска API Gateway и Redis"
                containerInstance api_gateway
                containerInstance user_cache
                properties {
                    "RAM" "4Gb"
                    "HDD" "16Gb"
                }
            }

            deploymentNode "node2" {
                description "Нода для запуска User Service"
                containerInstance user_service
                properties {
                    "RAM" "4Gb"
                    "HDD" "16Gb"
                }
            }

            deploymentNode "node3" {
                description "Нода для запуска Showcase Service"
                containerInstance showcase_service
                properties {
                    "RAM" "4Gb"
                    "HDD" "16Gb"
                }
            }

            deploymentNode "node4" {
                description "Нода для запуска Cart Service"
                containerInstance cart_service
                properties {
                    "RAM" "4Gb"
                    "HDD" "16Gb"
                }
            }

            deploymentNode "nodeN (N = 5, 6, 7)" {
                description "Нода для запуска СУБД - PostgreSQL и MongoDB"
                containerInstance user_db
                containerInstance showcase_db
                instances 3
                properties {
                    "RAM" "4Gb"
                    "HDD" "32Gb"
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

        // systemContext online_shop "systemContext" {
        //     include *
        //     autoLayout
        // }

        // container online_shop "container" {
        //     include *
        //     autoLayout
        // }

        // deployment online_shop "Production" "deployment" {
        //     include *
        //     autoLayout
        // }

        dynamic online_shop "UC01" "Создание нового пользователя" {
            autoLayout
            user -> front_service "Регистрация нового пользователя"
            front_service -> api_gateway "Отправка запроса с фронт-энда (POST user/)"
            api_gateway -> user_service "Проксирование запроса"
            user_service -> user_db "Сохранение данных пользователя"
            user_service -> user_cache "Сохранение данных пользователя в кэш"
        }

        dynamic online_shop "UC02" "Поиск пользователя по логину" {
            autoLayout
            user -> front_service "Поиск пользователя по {login} в интерфейсе"
            front_service -> api_gateway "Отправка запроса с фронт-энда (GET user/)"
            api_gateway -> user_service "Проксирование запроса"
            user_service -> user_db "Получение данных пользователя по {login}"
        }

        dynamic online_shop "UC03" "Поиск пользователя по маске имя и фамилии" {
            autoLayout
            user -> front_service "Поиск пользователя по {mask} в интерфейсе"
            front_service -> api_gateway "Отправка запроса с фронт-энда (GET user/)"
            api_gateway -> user_service "Проксирование запроса"
            user_service -> user_db "Получение данных пользователя по {mask}"
        }

        dynamic online_shop "UC04" "Создание товара" {
            autoLayout
            user -> front_service "Создание нового товара в интерфейсе"
            front_service -> api_gateway "Отправка запроса с фронт-энда (POST clothes/)"
            api_gateway -> showcase_service "Проксирование запроса"
            showcase_service -> showcase_db "Сохранение информации о товаре"
        }

        dynamic online_shop "UC05" "Получение списка товаров" {
            autoLayout
            user -> front_service "Получение списка товаров в интерфейсе"
            front_service -> api_gateway "Отправка запроса с фронт-энда (GET clothes/)"
            api_gateway -> showcase_service "Проксирование запроса"
            showcase_service -> showcase_db "Выгрузка списка товаров из СУБД"
        }

        dynamic online_shop "UC06" "Добавление товара в корзину" {
            autoLayout
            user -> front_service "Добавление товара в корзину в интерфейсе"
            front_service -> api_gateway "Отправка запроса с фронт-энда (POST cart/clothes/)"
            api_gateway -> cart_service "Проксирование запроса"
            cart_service -> user_db "Сохранение информации о корзине"
        }

        dynamic online_shop "UC07" "Получение корзины для пользователя" {
            autoLayout
            user -> front_service "Получение корзины для пользователя в интерфейсе"
            front_service -> api_gateway "Отправка запроса с фронт-энда (POST cart/user/)"
            api_gateway -> cart_service "Проксирование запроса"
            cart_service -> user_db "Выгрузка корзины для пользователя из СУБД"
        }

        styles {
            element "database" {
                shape cylinder
            }
        }
    }
}