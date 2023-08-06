## Usage
=> Create folders named `plugins`, `addons`, `assistant` and `resources`.<br/>
=> Add your plugins in the `plugins` folder and others accordingly.<br/>
=> Create a `.env` file with `API_ID`, `API_HASH`, `SESSION`, 
`BOT_TOKEN`, `BOT_USERNAME` as mandatory environment variables. Check
[`.env.sample`](https://github.com/TeamExtremePro/ExtremeProUserbot/.env.sample) for more details.<br/>
=> Run `python -m Extre` to start the bot.<br/>

### Creating plugins
To work everywhere

```python
@extremepro_cmd(
    pattern="start",
)   
async def _(e):   
    await eor(e, "extremepro Started")   
```

To work only in groups

```python
@extremepro_cmd(
    pattern="start",
    groups_only=True,
)   
async def _(e):   
    await eor(e, "ExtremePro Started")   
```

Assistant Plugins 👇

```python
@asst_cmd("start")   
async def _(e):   
    await e.reply("ExtremePro Started")   
```
