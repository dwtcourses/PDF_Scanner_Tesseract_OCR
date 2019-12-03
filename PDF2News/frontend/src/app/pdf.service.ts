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

  addPdf(username: string, file: File, description: string, tags: string) {
    const addPdf = gql`
      mutation addPdf(
        $username: String,
        $file: Upload!,
        $description: String,
        $tags: String
      ){
        addPdf(
          username: $username,
          file: $file,
          description: $description,
          tags: $tags
        ) {
          id,
          fileLocation,
          username,
          description,
          tags
        }
      }
    `;
    
    return this.apollo.mutate({
      mutation: addPdf,
      variables: {
        username,
        file,
        description,
        tags
      },
      context: {
        useMultipart: true
      }
    })
  }

  editPdf(id: number, file: File, description: string, tags: string) {
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
        ) {
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

  getPdfs(page: number = 1) {
    const getPdfs = gql`
      query getPdfs(
        $page: Int,
      ){
        getPdfs(
          page: $page
        ) {
          pdfs {
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
        page,
      }
    })
  }

  deletePdf(id: number) {
    const deletePdf = gql`
      mutation deletePdf(
        $id: Int,
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

  searchPdfs(searchQuery: string) {
    const getPdfs = gql`
      query searchPdfs(
        $searchQuery: String,
      ){
        searchPdfs(
          searchQuery: $searchQuery
        ) {
          pdfs {
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
        searchQuery,
      }
    })
  }
}
