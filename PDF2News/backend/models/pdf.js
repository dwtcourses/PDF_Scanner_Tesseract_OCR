'use strict';
module.exports = (sequelize, DataTypes) => {
  const Pdf = sequelize.define('Pdf', {
    sessionId: DataTypes.STRING,
    fileLocation: DataTypes.STRING,
    description: DataTypes.STRING,
    tags: DataTypes.STRING,
    status: DataTypes.STRING
  }, {});
  Pdf.associate = function(models) {
    // associations can be defined here
  };
  return Pdf;
};