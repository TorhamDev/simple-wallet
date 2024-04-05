# simple-wallet

> a simplified wallet service with a strange twist.

## NOTE

I know that Redis is not a good option for this project! probably RabbitMQ is a better option, but why do I use Redis and make a lot of problems for myself? bc I know Redis! I prefer using something I know instead of something I have no idea about, so that was why I used Redis in this project if you are wondering.

### things I want to do but I don't have time for it:

- [ ] Setup logger
- [ ] Swagger doc
- [ ] Complite testing
- [ ] Use somthing better than redis

### The main problem of this project

this project has a main problem and it starts with 3rd party service, we have to deposit to the user's bank account via a 3rd party API and make sure that both services are on the same page (our and 3rd party).
so if 3rd party has a problem with the deposit we have to roll back all of our work and what if 3rd party doesn't have any problem but we land a problem? this is not reminding you of something? yes, [Two Generals' Problem](https://www.designgurus.io/answers/detail/what-is-the-two-generals-problem)

so we know there is no real answer to this problem, there is always something wrong with this situation and I guess dealing with this problem was the main target of the project.
