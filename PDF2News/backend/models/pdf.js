'use strict';
module.exports = (sequelize, DataTypes) => {
  const Pdf = sequelize.define('Pdf', {
    cookieId: DataTypes.STRING,
    fileLocation: DataTypes.STRING,
    description: DataTypes.STRING,
    tags: DataTypes.STRING
  }, {});
  Pdf.associate = function(models) {
    // associations can be defined here
  };
  return Pdf;
};