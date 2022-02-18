import { ModelInit, MutableModel, PersistentModelConstructor } from "@aws-amplify/datastore";





type FileAccessMetaData = {
  readOnlyFields: 'createdAt' | 'updatedAt';
}

export declare class FileAccess {
  readonly id: string;
  readonly user: string;
  readonly date: string;
  readonly time: string;
  readonly filename: string;
  readonly createdAt?: string;
  readonly updatedAt?: string;
  constructor(init: ModelInit<FileAccess, FileAccessMetaData>);
  static copyOf(source: FileAccess, mutator: (draft: MutableModel<FileAccess, FileAccessMetaData>) => MutableModel<FileAccess, FileAccessMetaData> | void): FileAccess;
}