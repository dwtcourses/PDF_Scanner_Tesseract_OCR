const { buildSchema } = require('graphql');

export const schema = buildSchema( `
    scalar Upload

    type Pdf {
        id: Int,
        fileLocation: String,
        description: String,
        tags: String
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
        addPdf(file: Upload!, description: String, tags: String): Pdf
        editPdf(id: Int, file: Upload!, description: String, tags: String): Pdf
        deletePdf(id: Int): Int
    }
`);
