/**
 * {{PROJECT_NAME}}
 * {{PROJECT_DESCRIPTION}}
 */

import { config } from './lib/config.js';
import { logger } from './lib/logger.js';

async function main() {
  logger.info('Starting application', { env: config.env });

  // Initialize your application here
  // Example:
  // const db = await createDatabase(config.db);
  // const server = createServer({ db });
  // await server.listen(config.port);

  logger.info('Application started', { port: config.port });
}

main().catch((error) => {
  logger.error('Failed to start application', { error: String(error) });
  process.exit(1);
});
