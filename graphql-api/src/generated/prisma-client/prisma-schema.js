module.exports = {
        typeDefs: // Code generated by Prisma (prisma@1.34.10). DO NOT EDIT.
  // Please don't change this file manually but run `prisma generate` to update it.
  // For more information, please read the docs: https://www.prisma.io/docs/prisma-client/

/* GraphQL */ `type AggregatePdf {
  count: Int!
}

type BatchPayload {
  count: Long!
}

scalar DateTime

scalar Long

type Mutation {
  createPdf(data: PdfCreateInput!): Pdf!
  updatePdf(data: PdfUpdateInput!, where: PdfWhereUniqueInput!): Pdf
  updateManyPdfs(data: PdfUpdateManyMutationInput!, where: PdfWhereInput): BatchPayload!
  upsertPdf(where: PdfWhereUniqueInput!, create: PdfCreateInput!, update: PdfUpdateInput!): Pdf!
  deletePdf(where: PdfWhereUniqueInput!): Pdf
  deleteManyPdfs(where: PdfWhereInput): BatchPayload!
}

enum MutationType {
  CREATED
  UPDATED
  DELETED
}

interface Node {
  id: ID!
}

type PageInfo {
  hasNextPage: Boolean!
  hasPreviousPage: Boolean!
  startCursor: String
  endCursor: String
}

type Pdf {
  id: ID!
  createdAt: DateTime!
  updatedAt: DateTime!
  filename: String!
  text: String!
}

type PdfConnection {
  pageInfo: PageInfo!
  edges: [PdfEdge]!
  aggregate: AggregatePdf!
}

input PdfCreateInput {
  id: ID
  filename: String!
  text: String!
}

type PdfEdge {
  node: Pdf!
  cursor: String!
}

enum PdfOrderByInput {
  id_ASC
  id_DESC
  createdAt_ASC
  createdAt_DESC
  updatedAt_ASC
  updatedAt_DESC
  filename_ASC
  filename_DESC
  text_ASC
  text_DESC
}

type PdfPreviousValues {
  id: ID!
  createdAt: DateTime!
  updatedAt: DateTime!
  filename: String!
  text: String!
}

type PdfSubscriptionPayload {
  mutation: MutationType!
  node: Pdf
  updatedFields: [String!]
  previousValues: PdfPreviousValues
}

input PdfSubscriptionWhereInput {
  mutation_in: [MutationType!]
  updatedFields_contains: String
  updatedFields_contains_every: [String!]
  updatedFields_contains_some: [String!]
  node: PdfWhereInput
  AND: [PdfSubscriptionWhereInput!]
  OR: [PdfSubscriptionWhereInput!]
  NOT: [PdfSubscriptionWhereInput!]
}

input PdfUpdateInput {
  filename: String
  text: String
}

input PdfUpdateManyMutationInput {
  filename: String
  text: String
}

input PdfWhereInput {
  id: ID
  id_not: ID
  id_in: [ID!]
  id_not_in: [ID!]
  id_lt: ID
  id_lte: ID
  id_gt: ID
  id_gte: ID
  id_contains: ID
  id_not_contains: ID
  id_starts_with: ID
  id_not_starts_with: ID
  id_ends_with: ID
  id_not_ends_with: ID
  createdAt: DateTime
  createdAt_not: DateTime
  createdAt_in: [DateTime!]
  createdAt_not_in: [DateTime!]
  createdAt_lt: DateTime
  createdAt_lte: DateTime
  createdAt_gt: DateTime
  createdAt_gte: DateTime
  updatedAt: DateTime
  updatedAt_not: DateTime
  updatedAt_in: [DateTime!]
  updatedAt_not_in: [DateTime!]
  updatedAt_lt: DateTime
  updatedAt_lte: DateTime
  updatedAt_gt: DateTime
  updatedAt_gte: DateTime
  filename: String
  filename_not: String
  filename_in: [String!]
  filename_not_in: [String!]
  filename_lt: String
  filename_lte: String
  filename_gt: String
  filename_gte: String
  filename_contains: String
  filename_not_contains: String
  filename_starts_with: String
  filename_not_starts_with: String
  filename_ends_with: String
  filename_not_ends_with: String
  text: String
  text_not: String
  text_in: [String!]
  text_not_in: [String!]
  text_lt: String
  text_lte: String
  text_gt: String
  text_gte: String
  text_contains: String
  text_not_contains: String
  text_starts_with: String
  text_not_starts_with: String
  text_ends_with: String
  text_not_ends_with: String
  AND: [PdfWhereInput!]
  OR: [PdfWhereInput!]
  NOT: [PdfWhereInput!]
}

input PdfWhereUniqueInput {
  id: ID
}

type Query {
  pdf(where: PdfWhereUniqueInput!): Pdf
  pdfs(where: PdfWhereInput, orderBy: PdfOrderByInput, skip: Int, after: String, before: String, first: Int, last: Int): [Pdf]!
  pdfsConnection(where: PdfWhereInput, orderBy: PdfOrderByInput, skip: Int, after: String, before: String, first: Int, last: Int): PdfConnection!
  node(id: ID!): Node
}

type Subscription {
  pdf(where: PdfSubscriptionWhereInput): PdfSubscriptionPayload
}
`
      }
    