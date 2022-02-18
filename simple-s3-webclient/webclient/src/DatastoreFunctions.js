import { DataStore } from '@aws-amplify/datastore';
import { FileAccess } from '../models';
//
function Datastore(info) {
    
    const saveFile = async (info) => {

        await DataStore.save(
          new FileAccess({
            "user": info.email,
            "date": info.date,
            "time": info.time,
            "filename": info.filename
          })
        )
    };
    
    const updateFile = async (info) => {
        /* DataStore items are immutable. Update a record by making a copy of it
        and apply the updates to the new item's fields */
        await DataStore.save(FileAccess.copyOf(CURRENT_ITEM, item => {
            // Update the values on { item }
        }))
    }
    
    const deleteFile = async (info) => {
        const modelToDelete = await DtaStore.query(FileAccess, 123456789);
        DataStore.delete(modelToDelete);
    }
    
    const queryFiles = async (info) => {
        const models = await DataStore.query(FileAccess);
        console.log(models)
    }
}

export default Datastore;