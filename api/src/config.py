import os
from urllib.parse import quote
from pathlib import Path

from pydantic import ConfigDict, Field, SecretStr, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvConfigBase(BaseSettings):
    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        env_file=os.path.join(Path(__file__).resolve().parents[1], ".env"),
        env_file_encoding="utf-8",
    )


class DbConfig(EnvConfigBase):
    model_config = SettingsConfigDict(env_prefix='DB_')

    host: str
    port: int
    user: str
    password: SecretStr
    name: str

    @computed_field()
    def url(self) -> SecretStr:
        return SecretStr(
            f'postgresql+asyncpg://{quote(self.user)}:{quote(self.password.get_secret_value())}'
            f'@{self.host}:{self.port}/{self.name}'
        )


class Config(BaseSettings):
    db: DbConfig = Field(default_factory=DbConfig)

    @classmethod
    def load(cls):
        return cls()


settings = Config.load()
