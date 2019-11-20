import { Injectable } from '@angular/core';
import { Apollo } from 'apollo-angular';
import gql from 'graphql-tag';

@Injectable({
  providedIn: 'root'
})
export class PdfService {

  constructor(
    private apollo: Apollo
  ) { }

  // Create: Upload Pdf file
  addPdf (file: File, description: string, tags: string){
    const addPdf = gql`
      mutation addPdf(
        $file: Upload!,
        $description: String,
        $tags: String
      ){
        addPdf(
          file: $file,
          description: $description,
          tags: $tags
        ){
          id,
          fileLocation,
          description,
          tags
        }
      }
    `;

    return this.apollo.mutate({
      mutation: addPdf,
      variables: {
        file,
        description,
        tags
      },
      context: {
        useMultipart: true
      }
    })
  }

  // Read: Get Pdf
  getPdfs(page: number = 1){
    const getPdfs = gql`
      query getPdfs(
        $page: Int
      ){
        getPdfs(
          page: $page
        ){
          pdfs{
            id,
            fileLocation,
            description,
            tagsS
          },
          page,
          totalPdfs   
        }
      }
    `;

    return this.apollo.mutate({
      mutation: getPdfs,
      variables:{
        page
      }
    })
  }

  // Search Pdf
  searchPdfs(searchQuery: string){
    const getPdfs = gql`
      query searchPdfs(
        $searchQuery: String
      ){
        searchPdfs(
          searchQuery: $searchQuery
        ){
          pdfs{
            id, 
            fileLocation,
            description,
            tags
          },
          page,
          totalPdfs
        }
      }
    `;

    return this.apollo.mutate({
      mutation: getPdfs,
      variables: {
        searchQuery
      }
    })
  }

  // Update: Edit Pdf
  editPdf(id: number, file: File, description: string, tags: string){
    const editPdf = gql`
      mutation editPdf(
        $id: Int!,
        $file: Upload!,
        $description: String,
        $tags: String
      ){
        editPdf(
          id: $id,
          file: $file,
          description: $description,
          tags: $tags
        ){
          id, 
          fileLocation,
          description,
          tags
        }
      }
    `;

    return this.apollo.mutate({
      mutation: editPdf,
      variables: {
        id,
        file,
        description,
        tags
      },
      context: {
        useMultipart: true
      }
    })
  }

  // Delete: Remove Pdf
  deletePdf(id: number){
    const deletePdf = gql`
      mutation deletePdf(
        $id: Int
      ){
        deletePdf(
          id: $id
        )
      }
    `;

    return this.apollo.mutate({
      mutation: deletePdf,
      variables: {
        id,
      }
    })
  }
}