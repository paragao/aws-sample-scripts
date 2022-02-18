import './App.css';
import { useState, useEffect } from 'react';
import { DataStore } from '@aws-amplify/datastore';
import { FileAccess } from './models';
import { Storage, Auth, Hub } from 'aws-amplify';
import { 
  Authenticator, useTheme,
  Heading, Card, Flex, View, Divider, 
  Button, Text, SelectField,
  IconSave, Image, IconDelete,
  Table, TableCell, TableRow, TableHead, TableBody } from '@aws-amplify/ui-react';
//import { AmplifyS3Album, AmplifyS3TextPicker, AmplifyS3ImagePicker } from '@aws-amplify/ui-react/legacy';

import Amplify from 'aws-amplify';
import awsconfig from './aws-exports';
Amplify.configure(awsconfig)

function App() {
  
  useEffect(() => {
    },//value to return 
    []//dependecies
  );

  const [fileId, setFileId] = useState();
  const [formData, setFormData] = useState([]);
  const [publicUrls, setPublicUrls] = useState([]);
  const [privateUrls, setPrivateUrls] = useState([]);
  const [protectLevel, setProtectLevel] = useState();

  Hub.listen('auth', async (data) => {
    if (data.payload.event === 'signOut') {
      await DataStore.clear();
    }
  });

  const saveFileOnTable = async (e) => {
    try {
      await Storage.put(formData.name, formData, {
        level: protectLevel,
        contentType: formData.type
      })
      .then(async () => {
        const original = await DataStore.query(FileAccess, formData.name)

        await DataStore.save(
          FileAccess.copyOf(original, e)
        )
        .then((model) => console.info('new datastore model added ', model))
        .catch((err) => console.warn('updated model error ', err))
      })
      .catch((err) => console.warn('storage error ', err))
    } catch (err) { 
      console.log('error saving file on try/catch')
    }
  };

  const listFiles = async () => {
    console.info('listing files')

    await Storage.list('', { level: 'public' })
      .then((result) => {
        const publicSignedUrls = []
        
        result.forEach(async (elem) => {
          if (elem.key !== "") {
            const item = await Storage.get(elem.key)
            const id = await DataStore.query(FileAccess, c => c.filename("eq", elem.key))
            publicSignedUrls.push({'key': elem.key, 'url': item, 'id': id })
          }
        })

        setPublicUrls(publicSignedUrls)
      })
      .catch((err) => console.error(err))
    
    await Storage.list('', { level: 'private' })
      .then((result) => {
        const privateSignedUrls = []
        
        result.forEach(async (elem) => {
          if (elem.key !== "") {
            const item = await Storage.get(elem.key)
            const id = await DataStore.query(FileAccess, c => c.filename("eq", elem.key))
            privateSignedUrls.push({ 'key': elem.key, 'url': item, 'id': id })
          }
        })
        
        setPrivateUrls(privateSignedUrls)
      })
      .catch((err) => console.error(err))
  }

  const deleteFile = async (f) => {
    console.log('url id ', f)
    const modelToDelete = await DataStore.query(FileAccess, f);
    DataStore.delete(modelToDelete);
  };
  
  const queryFiles = async () => {
    const models = await DataStore.query(FileAccess);
    console.log('datastore model and datastore sync ', models)
  };

  const handleSaveFile = async (event) => {
    const user = await Auth.currentAuthenticatedUser();
    const email = user.attributes.email

    const date = new Date()
    const awsDate = date.toISOString().split("T")[0]
    const awsTime = date.toISOString().split("T")[1] 

    const params = {
      "user": email,
      "date": awsDate,
      "time": awsTime,
      "filename": formData ? formData.name : null
    } 
    
    if (Object.entries(params).length === 0) {
      console.warn('data is empty ', params)
    } else {
      console.info('protect level ', protectLevel)
      saveFileOnTable(params)
      
    }
  }

  const handleQueryData = () => {
    queryFiles()
  }

  const handleDeleteData = () => {
    if (fileId) {
      deleteFile(fileId)
    } else {
      console.warn('File ID required to delete data from DataStore.')
    }
  }

  const components = {
    Header() {
      const { tokens } = useTheme();

      return(
        <View textAlign="center" padding={tokens.space.large}>
          <Image alt="Amplify logo" src="https://docs.amplify.aws/assets/logo-dark.svg" />
        </View>
      );
    },
    Footer() {
      const { tokens } = useTheme();

      return(
        <View textAlign="center" padding={ tokens.space.large}>
          <Text color={ `${tokens.colors.neutral['80']}`}>2021 &copy; All Rights Reserved</Text>
        </View>
      )
    }
  }

  const FileTable = (obj) => {

    if (obj.area === "private") {
      const files = privateUrls
      console.log('private Urls ', privateUrls)
      return(
        <Table variation="bordered" highlightOnHover={true} key="private-files-list">
          <TableHead>
            <TableRow>
              <TableCell as="th" maxWidth="50px"></TableCell>
              <TableCell as="th" maxWidth="50px"></TableCell>
              <TableCell as="th" minWidth="350px">Filename</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {
              files.map((url, index) => 
                <TableRow key={index}>
                  <TableCell>
                    <Button as="a" href={url.url}><IconSave /></Button>
                  </TableCell>
                  <TableCell>
                    <Button onClick={deleteFile}><IconDelete /></Button>
                  </TableCell>
                  <TableCell>{url.key}</TableCell>
                </TableRow>
              )
            }
          </TableBody>
        </Table>
      )
    }
    if (obj.area === "public") {
      const files = publicUrls
      console.log('public Urls ', publicUrls)
      return(
        <Table variation="bordered" highlightOnHover={true} key="public-files-list">
          <TableHead>
            <TableRow>
              <TableCell as="th" maxWidth="50px"></TableCell>
              <TableCell as="th" maxWidth="50px"></TableCell>
              <TableCell as="th" minWidth="350px">Filename</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {
              files.map((url, index) => 
                <TableRow key={index}>
                  <TableCell>
                    <Button as="a" href={url.url}><IconSave /></Button>
                  </TableCell>
                  <TableCell>
                    <Button onClick={(url) => deleteFile(url.id)}><IconDelete /></Button>
                  </TableCell>
                  <TableCell>{url.key}</TableCell>
                </TableRow>
              )
            }
          </TableBody>
        </Table>
      )
    }
  }

  const handleProtectLevel = (event) => {
    console.log('event level ', event.target.value)
    setProtectLevel(event.target.value)
  }
  return (
    <Authenticator components={components} signUpAttributes={['name']}>
      {({ signOut, user }) => (
        <View textAlign="center" key="top-card">
          <Flex direction="column" alignItems="center">
            <Card variation="elevated">
              <Heading level={4}>Simple Amazon S3 web client using AWS Amplify</Heading>
              <Divider size="large" padding="5px" />
              <Flex as="form" direction="column" padding="5px" margin="5px 0 0 0">
                  <Button as="input" type="file" onChange={(e) => setFormData(e.target.files[0])} />
                  <SelectField label="protectLevel" labelHidden={true} onChange={handleProtectLevel}>
                    <option value="private">Private (only user can read/write)</option>
                    <option value="protected">Protected (public read but only user can write)</option>
                    <option value="public">Public (public read/write)</option>
                  </SelectField>
                  <Button type="sumbit" onClick={handleSaveFile} value={user.username}>Upload file</Button>
              </Flex>
              <Flex padding="5px">
                <Button onClick={handleQueryData}>
                  <label>Query datastore</label>
                </Button>
                <Button onClick={handleDeleteData}>
                  <label>Delete data</label>
                </Button>
                <Button onClick={listFiles}>
                  <label>List All Files</label>
                </Button>
                <Button onClick={signOut}>Sign Out</Button>
              </Flex>
            </Card>
            <Card variation="elevated" key="main-file-list">
              <Flex direction="row" justifyContent="space-around">
                <View padding="5px" minWidth="400px" textAlign="left" key="public-files">
                  <Heading textAlign="center">Public Files</Heading>
                  <FileTable area="public" key="public-files-listing" />
                </View>
                <View padding="5px" minWidth="400px" textAlign="left" key="private-files">
                  <Heading textAlign="center">Private Files</Heading>
                  <FileTable area="private" key="private-files-listing" />
                </View>
              </Flex>
            </Card>
          </Flex>
        </View>
      )}
    </Authenticator>
  );
}

export default App;
