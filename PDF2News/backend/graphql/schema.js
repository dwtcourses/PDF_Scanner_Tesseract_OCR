const { buildSchema } = require('graphql');

export const schema = buildSchema( `
    scalar Upload

    type Pdf {
        id: Int,
        sessionId: String,
        fileLocation: String,
        description: String,
        tags: String,
        status: String
    }

    type PdfData {
        pdfs: [Pdf],
        page: Int,
        totalPdfs: Int
    }

    type Query {
        getPdfs(page: Int): PdfData,
        searchPdfs(searchQuery: String): PdfData
    }

    type Mutation {
        addPdf(sessionId: String, file: Upload!, description: String, tags: String, status: String): Pdf
        editPdf(id: Int, file: Upload!, description: String, tags: String): Pdf
        deletePdf(id: Int): Int
    }
`);
