'use strict';
module.exports = (sequelize, DataTypes) => {
  const Pdf = sequelize.define('Pdf', {
    fileLocation: DataTypes.STRING
  }, {});
  Pdf.associate = function(models) {
    // associations can be defined here
  };
  return Pdf;
};