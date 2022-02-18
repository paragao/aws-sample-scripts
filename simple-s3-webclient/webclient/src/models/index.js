// @ts-check
import { initSchema } from '@aws-amplify/datastore';
import { schema } from './schema';



const { FileAccess } = initSchema(schema);

export {
  FileAccess
};