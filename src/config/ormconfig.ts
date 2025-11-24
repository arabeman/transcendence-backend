// src/config/ormconfig.ts
import { DataSourceOptions } from 'typeorm';

const config: DataSourceOptions = {
    type: 'sqlite',
    database: 'data/database.sqlite',
    entities: ['dist/entities/**/*.js'],
    migrations: ['dist/migrations/**/*.js'],
    synchronize: true, // only dev mode
};

export default config;
