const Op = require('sequelize').Op;

// Model 
const models = require('../models');
const fs = require('fs');

const storeFS = ({stream, filename}) => {
    const uploadDir = '../backend/pdfs';
    const path = `${uploadDir}/${filename}`;
    return new Promise((resolve, reject) => 
    stream
    .on('error', error => {
        if (stream.truncated)
            // delete the truncated file
            fs.unlinkSync(path);
        reject(error);
    })
    .pipe(fs.createWriteStream(path))
    .on('error', error => reject(error))
    .on('finish', () => resolve({path}))
    );
}

// Read PDF
export const getPdfs = async(args) => {
    const page = args.page;
    const pdfs = await models.PDF2News.findAll({
        offset: (page - 1) * 10,
        limit: 10,
    });

    const totalPdfs = await models.PDF2News.count();
    return {
        pdfs,
        page,
        totalPdfs
    };
}

// Create PDF
export const addPdf = async (args) => {
    const {description, tags} = args;
    const {filename, mimetype, createReadStream} = await args.file;
    const stream = createReadStream();
    const pathObj = await storeFS({stream, filename});
    const fileLocation = pathObj.path;
    const pdf = await models.PDF2News.create({
        fileLocation,
        description,
        tags
    })
}

// Update PDF
export const editPdf = async (args) => {
    const { id, description, tags } = args;
    const { filename, mimetype, createReadStream } = await args.file;
    const stream = createReadStream();
    const pathObj = await storeFS({ stream, filename });
    const fileLocation = pathObj.path;
    const pdf = await models.PDF2News.update({
        fileLocation,
        description,
        tags
    }, {
            where: {
                id
            }
        })
    return pdf;
}

// Delete PDF
export const deletePdf = async (args) => {
    const {id} = args;
    await models.PDF2News.destroy({
        where:{
            id
        }
    })
    return id;
}

// Search PDF
export const searchPdfs = async (args) => {
    const searchQuery = args.searchQuery;
    const pdfs = await models.PDF2News.findAll({
        where:{
            [Op.or]:[
                {
                    description:{
                        [Op.like]: `%${searchQuery}%`
                    }
                },
                {
                    tags:{
                        [Op.like]: `%${searchQuery}%`
                    }
                }
            ]
        }
    });
    const totalPdfs = await models.PDF2News.count();
    return {
        pdfs,
        totalPdfs,
    };
}

