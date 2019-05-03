# kimetaro

Kimetaro is the BOT which selects one of lists(Discord/Slack)

## How to introduce

1. Access the authorization page.(https://discordapp.com/api/oauth2/authorize?client_id=569752486483591168&permissions=0&scope=bot)
2. Select the server which you would like to register.
   ![OAuth](./img/OAuth.png)
3. Done

## How to operate

#### Call

```bash
/hey
決め太郎「おーきに」
```

#### Register

```bash
/add planA planB
/add "planA" "planB"
```
NOTE:
`"` (Double quotation) and no quotation can not be mixed
`'` (Single quotation) not accepted

#### List(Not implemented)

```bash
/list
 1. planA
 2. planB
```

#### Kimetaro(Not implemented)

```bash
/choice
 ～面白い演出
 決め太郎「決めたで！ planBや」
```

#### Bye(Not implemented)

```bash
/bye
決め太郎「ほな」
```

## For developper
`kimetaro` loads the discord of access token from environment values.
You debug or run `kimetaro` on your environment, necessary to set your access token as environment values.
I recommend you to use `direnv`, which set environment values automatically.

1. Please modify `.envrc.sample` as following
```bash
$ vim .envrc.sample
[TOKEN]
ACCESSTOKEN=YOUR_DISCORD_ACCESS_TOKEN
```
2. Rename `.envrc.sample` to `.envrc`.
3. Run kimetaro
```bash
$ python3 kimetaro.py
```

Ref [direnv](https://github.com/direnv/direnv)

