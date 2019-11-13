const {GraphQLServer} = require('graphql-yoga')

let pdfs = [
    {
        id: 'pdf-0',
        filename: 'sample_pdf',
        text: 'at completeObjectValue (/Users/ericleung/Desktop/Comp/Project/PDF_Scanner_Tesseract_OCR/graphql-api/node_modules/graphql/execution/execute.js:703:10)'
    },
    {
        id: 'pdf-0',
        filename: 'sample_pdf',
        text: 'LICENSE         README.md       graphql-api     nlp_analysis.py ocr.py'
    },
]

let idCount = pdfs.length

const resolvers = {
    Query: {
      info: () => `This is the API of a Hackernews Clone`,
      pdfs: () => pdfs,
    },
    // Mutation: {
    //   // 2
    //   post: (parent, args) => {
    //      const link = {
    //       id: `link-${idCount++}`,
    //       description: args.description,
    //       url: args.url,
    //     }
    //     links.push(link)
    //     return link
    //   }
    // },
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