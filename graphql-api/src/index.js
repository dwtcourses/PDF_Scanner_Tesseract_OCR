const {GraphQLServer} = require('graphql-yoga')
const { prisma } = require('./generated/prisma-client')

// Dummy data
// let pdfs = [
//     {
//         id: 'pdf-1',
//         filename: 'sample_pdf1',
//         text: 'at completeObjectValue (/Users/ericleung/Desktop/Comp/Project/PDF_Scanner_Tesseract_OCR/graphql-api/node_modules/graphql/execution/execute.js:703:10)'
//     },
//     {
//         id: 'pdf-2',
//         filename: 'sample_pdf2',
//         text: 'LICENSE         README.md       graphql-api     nlp_analysis.py ocr.py'
//     },
// ]

const resolvers = {
    Query: {
      info: () => `This is a GraphQL api`,
      pdfs: (root, args, context, info) => {
          return context.prisma.pdfs()
      },
    //   pdf:  (_, {id}) => {
    //       const pdf = pdfs.find(pdf => pdf.id === id)
    //       return pdf;
    //   },
    },
    Mutation: {
      post: (root, args, context) => {
         return context.prisma.createpDF({
             filename: args.filename,
             text: args.text,
         })
      },
    },
    Pdf: {
        id: (parent) => parent.id,
        filename: (parent) => parent.filename,
        text: (parent) => parent.text,
    }
}

const server = new GraphQLServer({
    typeDefs: './src/schema.graphql',
    resolvers,
    context: { prisma },
})

server.start(() => console.log(`Listening for requests on Port 4000`))