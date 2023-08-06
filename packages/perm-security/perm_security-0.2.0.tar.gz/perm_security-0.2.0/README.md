
# Perm-Security

#### A package to enable the integration between Discord's API and Perm-Banana

#### Features
- Permission classes for converting Discord's Permissions to Perm-Banana
- Member Adapters to enable Perm-Banana's extended functionality
- The ability to create Tokens
- A TokenStrategy for handling Permissions with Discord's API

#### How to use it?

```python
from discord import Member
from discord.ext.commands import Cog, Greedy, Context, command

from perm_security.converters import PermissionChannelConverter
from perm_security.MemberAdapter import MemberChannelAdapter
from perm_security.TokenStrategy import BasicTokenStrategy
from perm_security.TokenStrategy.TokenHandlerStrategy import BasicTokenHandlerStrategy

class Security(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.token_strategy = BasicTokenStrategy(BasicTokenHandlerStrategy(bot.scheduler))

    @command(name="generate_toke")
    async def generate_token(
        self,
        ctx: Context,
        permissions: PermissionChannelConverter,
        members: Greedy[Member],
        uses: int = 1
        duration: float = 60.0
    ):
        author = MemberChannelAdapter(ctx.author, ctx.channel)
        await self.token_strategy.generate_token(author, permissions, members, uses, duration)
```
