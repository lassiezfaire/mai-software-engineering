workspace {
    name "Магазин"
    description "Лабораторная работа 01"

    model {
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
                technology "Python / REST API"
            }

            group "Слой данных" {
                user_db = container "User Database" {
                    description "Реляционная СУБД, содержащая информацию о пользователях"
                    technology "PostgreSQL"
                    tags "database"
                }

                user_cache = container "User Cache Database" {
                    description "Кеш данных, хранимый для ускорения поиска информации о пользователях"
                    technology "Redis"
                    tags "database"
                }

                shop_db = container "Goods and Cart Database" {
                    description "Документоориентированная СУБД, содержащая информацию о товарах и о корзинах пользователей"
                    technology "MongoDB"
                    tags "database"
                }
            }

            api_app -> user_db "Получение или обновление данных о пользователе" "TCP:5432"
            api_app -> user_cache "Получение или обновление данных о пользователе" "TCP:6379"
            api_app -> shop_db "Получение или обвноление данных о товаре и о корзине пользователя" "TCP:27017"

            user -> api_app "Просмотр товаров и добавление их в корзину" "REST HTTP:8000"
            shop_owner -> api_app "Добавление товара в магазин" "REST HTTP:8000"
        }

        deploymentEnvironment "Production" {
            
            deploymentNode "node0" {
                description "Главная нода для запуска REST API приложения и Redis"
                containerInstance api_app
                containerInstance user_cache
                properties {
                    "RAM" "4Gb"
                    "HDD" "16Gb"
                }
            }

            deploymentNode "nodeN (N = 1, 2, 3)" {
                description "Нода для запуска СУБД - PostgreSQL и MongoDB"
                containerInstance user_db
                containerInstance shop_db
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

        dynamic online_shop "UC01" "Создание нового пользователя" {
            autoLayout
            user -> api_app "Регистрация нового пользователя (POST /user)"
            api_app -> user_db "Сохранение данных пользователя"
            api_app -> user_cache "Сохранение данных пользователя в кэш"
        }

        dynamic online_shop "UC02" "Поиск пользователя по логину" {
            autoLayout
            user -> api_app "Поиск пользователя по {login}  (GET /user)"
            api_app -> user_cache "Получение данных пользователя по {login}"
            api_app -> user_db "Получение данных пользователя по {login}, если их не было в кэше"
        }

        dynamic online_shop "UC03" "Поиск пользователя по маске имя и фамилии" {
            autoLayout
            user -> api_app "Поиск пользователя по {mask}  (GET /user)"
            api_app -> user_cache "Получение данных пользователя по {mask}"
            api_app -> user_db "Получение данных пользователя по {mask}, если их не было в кэше"
        }

        dynamic online_shop "UC04" "Создание товара" {
            autoLayout
            shop_owner -> api_app "Создание нового товара (POST /good)"
            api_app -> shop_db "Сохранение информации о товаре"
        }

        dynamic online_shop "UC05" "Получение списка товаров" {
            autoLayout
            shop_owner -> api_app "Получение списка товаров (GET /good)"
            api_app -> shop_db "Выгрузка списка товаров из СУБД"
        }

        dynamic online_shop "UC06" "Добавление товара в корзину" {
            autoLayout
            user -> api_app "Добавление товара в корзину (POST /cart/good)"
            api_app -> shop_db "Сохранение информации о корзине"
        }

        dynamic online_shop "UC07" "Получение корзины для пользователя" {
            autoLayout
            user -> api_app "Получение корзины для пользователя (POST /cart/good)"
            api_app -> shop_db "Выгрузка корзины для пользователя из СУБД"
        }

        styles {
            element "database" {
                shape cylinder
            }
        }
    }
}