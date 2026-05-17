# Data Sources

| Chain | Data | Source | Auth Required |
|---|---|---|---|
| Stellar | Ledger stats, TPS | Horizon API (horizon.stellar.org) | No |
| Bitcoin | Hashrate, tx count | mempool.space API | No |
| Ethereum | Validator count | Beaconcha.in API | No (rate-limited) |
| Cardano | Stake pool count, tx count | Blockfrost API | Yes — free tier |
| Solana | Validator count, TPS | Solana public RPC | No |
| All chains | Carbon intensity | Electricity Maps API | Yes — free tier |

## Getting API Keys

**Blockfrost (Cardano):**
1. Sign up at https://blockfrost.io
2. Create a mainnet project
3. Copy the project ID to `.env` as `BLOCKFROST_PROJECT_ID`

**Electricity Maps:**
1. Sign up at https://electricitymaps.com
2. Request a free API key
3. Copy to `.env` as `ELECTRICITY_MAPS_API_KEY`

Without these keys the pipeline still runs using placeholder values and skips carbon annotation.
