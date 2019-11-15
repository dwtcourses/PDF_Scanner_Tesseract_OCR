const Express = require("express");
const ExpressGraphQL = require("express-graphql");
const Mongoose = require("mongoose");
const {
    GraphQLID,
    GraphQLString,
    GraphQLList,
    GraphQLNonNull,
    GraphQLObjectType,
    GraphQLSchema,
} = require("graphql");

let app = Express();

Mongoose.connect("mongodb://localhost:27017/test", {useNewUrlParser: true});

const PdfModel = Mongoose.model("pdf", {
    filename: String,
    text: String
});

const PdfType = new GraphQLObjectType({ 
    name: "Pdf",
    fields: {
        filename: { type: GraphQLID },
        text: { type: GraphQLString }
    }
});

const schema = new GraphQLSchema({
    query: new GraphQLObjectType({
        name: "Query",
        fields: {
            pdfs: {
                type: GraphQLList(PdfType),
                resolve: (root, args, context, info) => {
                    return PdfModel.find().exec();
                }
            },
            pdf: {
                type: PdfType,
                args: {
                    filename: { type: GraphQLNonNull(GraphQLID) }
                },
                resolve: (root, args, context, info) => {
                    return PdfModel.findById(args.filename).exec();
                }
            }
        }
    }),
    mutation: new GraphQLObjectType({
        name: "Mutation",
        fields: {
            uploadPdf: {
                type: PdfType,
                args: {
                    filename: { type: GraphQLNonNull(GraphQLID) },
                    text: { type: GraphQLString }
                },
                resolve: (root, args, context, info) => {
                    const pdf = new PdfModel(args);
                    return pdf.save();
                }
            }
        }
    })
});

app.use("", ExpressGraphQL({
    schema: schema,
    graphiql: true
}));

app.listen(4000, () => {
    console.log("Listening at Port:4000...");
});