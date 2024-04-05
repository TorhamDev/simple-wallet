# simple-wallet

> a simplified wallet service with a strange twist.

## NOTE

I know that Redis is not a good option for this project! probably RabbitMQ is a better option, but why do I use Redis and make a lot of problems for myself? bc I know Redis! I prefer using something I know instead of something I have no idea about, so that was why I used Redis in this project if you are wondering.

### things I want to do but I don't have time for it:

- [ ] Dockerizing the project
- [ ] Setup logger
- [ ] Swagger doc
- [ ] Complite testing
- [ ] Use somthing better than redis

### The main problem of this project

this project has a main problem and it starts with 3rd party service, we have to deposit to the user's bank account via a 3rd party API and make sure that both services are on the same page (our and 3rd party).
so if 3rd party has a problem with the deposit we have to roll back all of our work and what if 3rd party doesn't have any problem but we land a problem? this is not reminding you of something? yes, [Two Generals' Problem](https://www.designgurus.io/answers/detail/what-is-the-two-generals-problem)

so we know there is no real answer to this problem, there is always something wrong with this situation and I guess dealing with this problem was the main target of the project.

![image](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)
![MySQL](https://img.shields.io/badge/mysql-4479A1.svg?style=for-the-badge&logo=mysql&logoColor=white)
![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white)
