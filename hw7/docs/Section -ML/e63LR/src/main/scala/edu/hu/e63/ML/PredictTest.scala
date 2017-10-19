package edu.hu.e63.ML

/*
 * PredictTest - Predictor Class to look at Test Data or any Random data and 
 * predict Evergreen Vs Ephemeral Pages on Data that do not have labels 
 * 
 * 
 */

import org.apache.spark._
import org.apache.spark.SparkContext
import org.apache.spark.mllib.classification.{ LogisticRegressionWithLBFGS, LogisticRegressionModel }
import org.apache.spark.mllib.evaluation.MulticlassMetrics
import org.apache.spark.mllib.regression.LabeledPoint
import org.apache.spark.mllib.linalg.Vectors
import org.apache.spark.mllib.util.MLUtils
import org.apache.spark.mllib.regression.LinearRegressionWithSGD
import org.apache.spark.mllib.classification.LogisticRegressionWithSGD
import org.apache.spark.mllib.classification.SVMWithSGD
import org.apache.spark.mllib.classification.NaiveBayes
import org.apache.spark.mllib.tree.DecisionTree
import org.apache.spark.mllib.tree.configuration.Algo
import org.apache.spark.mllib.tree.impurity.Entropy
import org.apache.spark.mllib.evaluation.BinaryClassificationMetrics //Notice
import org.apache.spark.mllib.linalg.distributed.RowMatrix //BetterLR
import org.apache.spark.mllib.feature.StandardScaler
import java.io.File
import org.apache.commons.io._;

object PredictTest {
  def main(args: Array[String]) {

    // Create a Scala Spark Context.

    val conf = new SparkConf().setMaster("local[*]").setAppName("All Models")
    val sc = new SparkContext(conf)

    try {
      FileUtils.deleteDirectory(new File("./data/*Data*"))
      println("Files Deleted ")
    } catch {
      case _: Throwable => println("Something is really wrong")
    }
    // Read the train file , its a tsv file with header
    // Remove header and split on tabs

    val rawtestrdd = sc.textFile("./data/test.tsv")
    val header = rawtestrdd.first()
    val testrdd = rawtestrdd.filter(_ != header)
    val cleantestrdd = testrdd.map(x => x.split("\t"))
    val categories = cleantestrdd.map(r => r(3)).distinct.collect.zipWithIndex.toMap
    println(categories.toVector)
    val numCategories = 14 //Array matching 

    val data = cleantestrdd.map { r =>
      val trimmed = r.map(_.replaceAll("\"", ""))
      val label = 0
      val categoryIdx = categories(r(3))
      val categoryFeatures = Array.ofDim[Double](numCategories)
      categoryFeatures(categoryIdx) = 1.0
      // println(categoryFeatures.toVector)
      val otherFeatures = trimmed.slice(4, r.size).map(d => if (d == "?") 0.0 else d.toDouble)

      val features = categoryFeatures ++ otherFeatures
      LabeledPoint(label, Vectors.dense(features))
    }

    val scalerCats = new StandardScaler(withMean = true, withStd = true).fit(data.map(lp => lp.features))
    val scaledTestData = data.map(lp => LabeledPoint(lp.label, scalerCats.transform(lp.features)))
    println(data.first.features)
    println(scaledTestData.first.features)

    val NewlrModel = LogisticRegressionModel.load(sc, "./model/LRModel")
    val numIterations = 20

    val prediction = NewlrModel.predict(scaledTestData.first.features)

    println("Predict - " + prediction)

    val LrPredict = scaledTestData.map { point =>
      if (NewlrModel.predict(point.features) == 1) 1 else 0
    }.countByValue()

    println("Total Test Data - " + data.count())
    LrPredict.keys.foreach { i =>
      if (i == 1)
        println("Ever Green Pages - " + LrPredict(i))
      else
        println("Ephemeral Pages - " + LrPredict(i))
    }
  }  

}