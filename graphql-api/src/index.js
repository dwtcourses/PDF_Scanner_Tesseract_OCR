const {GraphQLServer} = require('graphql-yoga')

let pdfs = [
    {
        id: 'pdf-0',
        filename: 'sample_pdf1',
        text: 'at completeObjectValue (/Users/ericleung/Desktop/Comp/Project/PDF_Scanner_Tesseract_OCR/graphql-api/node_modules/graphql/execution/execute.js:703:10)'
    },
    {
        id: 'pdf-0',
        filename: 'sample_pdf2',
        text: 'LICENSE         README.md       graphql-api     nlp_analysis.py ocr.py'
    },
]

let idCount = pdfs.length

const resolvers = {
    Query: {
      info: () => `This is a GraphQL api`,
      pdfs: () => pdfs,
      pdf:  (_, {id}) => {
          const pdf = pdfs.find(pdf => pdf.id === id)
          return pdf;
      },
    },
    Mutation: {
      // 2
      post: (parent, args) => {
         const pdf = {
          id: `pdf-${idCount++}`,
          filename: args.filename,
          text: args.text,
        }
        pdfs.push(pdf)
        return pdf
      }
    },
    PDF: {
        id: (parent) => parent.id,
        filename: (parent) => parent.filename,
        text: (parent) => parent.text,
    }
}

const server = new GraphQLServer({
    typeDefs: './src/schema.graphql',
    resolvers,
})

server.start(() => console.log(`Listening for requests on Port 4000`))