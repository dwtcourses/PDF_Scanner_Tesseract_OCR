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

  addPdf(sessionId: string, file: File, description: string, tags: string, status: string) {
    const addPdf = gql`
      mutation addPdf(
        $sessionId: String,
        $file: Upload!,
        $description: String,
        $tags: String,
        $status: String
      ){
        addPdf(
          sessionId: $sessionId,
          file: $file,
          description: $description,
          tags: $tags,
          status: $status
        ) {
          id,
          fileLocation,
          sessionId,
          description,
          tags,
          status
        }
      }
    `;
    
    return this.apollo.mutate({
      mutation: addPdf,
      variables: {
        sessionId,
        file,
        description,
        tags,
        status
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
