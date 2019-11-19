'use strict';
module.exports = (sequelize, DataTypes) => {
  const PDF2News = sequelize.define('PDF2News', {
    fileLocation: DataTypes.STRING,
    description: DataTypes.STRING,
    tags: DataTypes.STRING
  }, {});
  PDF2News.associate = function(models) {
    // associations can be defined here
  };
  return PDF2News;
};