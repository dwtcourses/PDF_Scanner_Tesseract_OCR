const Op = require('sequelize').Op;
const models = require('../models');
const fs = require('fs');

const storeFS = ({ stream, filename }) => {
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
            .on('finish', () => resolve({ path }))
    );
}

export const getPdfs = async (args) => {
    const page = args.page;
    const pdfs = await models.Pdf.findAll({
        offset: (page - 1) * 10,
        limit: 10
    });
    const totalPdfs = await models.Pdf.count();
    return {
        pdfs,
        page,
        totalPdfs
    };
}

export const addPdf = async (args) => {
    const { description, tags } = args;
    const { filename, mimetype, createReadStream } = await args.file;
    const stream = createReadStream();
    const pathObj = await storeFS({ stream, filename });
    const fileLocation = pathObj.path;
    const pdf = await models.Pdf.create({
        fileLocation,
        description,
        tags
    })
    return pdf;
}


export const editPdf = async (args) => {
    const { id, description, tags } = args;
    const { filename, mimetype, createReadStream } = await args.file;
    const stream = createReadStream();
    const pathObj = await storeFS({ stream, filename });
    const fileLocation = pathObj.path;
    const pdf = await models.Pdf.update({
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

export const deletePdf = async (args) => {
    // const { filename, mimetype, createReadStream } = await args.file;
    // const uploadDir = '../backend/pdfs';
    // const path = `${uploadDir}/${filename}`;
    const { id } = args;

    // Remove file from DB
    await models.Pdf.destroy({
        where: {
            id
        }
    })
    
    // Remove file in the user upload directory
    // await fs.unlink(path, (error) => {
    //     if (error){
    //         console.log(error);
    //         return;
    //     }
    // })

    return id;
}

export const searchPdfs = async (args) => {
    const searchQuery = args.searchQuery;
    const pdfs = await models.Pdf.findAll({
        where: {
            [Op.or]: [
                {
                    description: {
                        [Op.like]: `%${searchQuery}%`
                    }
                },
                {
                    tags: {
                        [Op.like]: `%${searchQuery}%`
                    }
                }
            ]
        }

    });
    const totalPdfs = await models.Pdf.count();
    return {
        pdfs,
        totalPdfs
    };
}