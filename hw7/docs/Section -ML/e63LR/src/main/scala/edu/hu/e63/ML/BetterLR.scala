package edu.hu.e63.ML

/*
 * BetterLR - Improvement in Model performamce with scaled Data 
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

object BetterLR {
  def main(args: Array[String]) {

    // Create a Scala Spark Context.

    val conf = new SparkConf().setMaster("local[*]").setAppName("All Models")
    val sc = new SparkContext(conf)

    try {

      val Directories = Array("./data/rawDataCatagoriesRDD", "./data/scaledDataCatagoriesRDD")
      for (x <- Directories) {
        FileUtils.deleteDirectory(new File(x))
      }
      println("Files Deleted ")
    } catch {
      case _: Throwable => println("Something is really wrong")
    }
    // Read the train file , its a tsv file with header
    // Remove header and split on tabs

    val rawtrainrdd = sc.textFile("./data/train.tsv")
    val header = rawtrainrdd.first()
    val trainrdd = rawtrainrdd.filter(_ != header)
    val cleantrainrdd = trainrdd.map(x => x.split("\t"))
    val numIterations = 20

    // Investigate the impact of adding in the 'category' feature
    val categories = cleantrainrdd.map(r => r(3)).distinct.collect.zipWithIndex.toMap
    // categories: scala.collection.immutable.Map[String,Int] = Map("weather" -> 0, "sports" -> 6, 
    //	"unknown" -> 4, "computer_internet" -> 12, "?" -> 11, "culture_politics" -> 3, "religion" -> 8,
    // "recreation" -> 2, "arts_entertainment" -> 9, "health" -> 5, "law_crime" -> 10, "gaming" -> 13, 
    // "business" -> 1, "science_technology" -> 7)
    val numCategories = categories.size

    val dataCategories = cleantrainrdd.map { r =>
      val trimmed = r.map(_.replaceAll("\"", ""))
      val label = trimmed(r.size - 1).toInt
      val categoryIdx = categories(r(3))
      val categoryFeatures = Array.ofDim[Double](numCategories)
      categoryFeatures(categoryIdx) = 1.0
      val otherFeatures = trimmed.slice(4, r.size - 1).map(d => if (d == "?") 0.0 else d.toDouble)
      val features = categoryFeatures ++ otherFeatures
      LabeledPoint(label, Vectors.dense(features))
    }
    dataCategories.cache()
      .coalesce(1, true)
      .saveAsTextFile("./data/rawDataCatagoriesRDD")

    val numDataCatagories = dataCategories.count
    println(dataCategories.first)

    // standardize the feature vectors
    val scalerCats = new StandardScaler(withMean = true, withStd = true).fit(dataCategories.map(lp => lp.features))
    val scaledDataCats = dataCategories.map(lp => LabeledPoint(lp.label, scalerCats.transform(lp.features)))
    println(dataCategories.first.features)
    println(scaledDataCats.first.features)

    // We will use this in LRModelsParmImpact class
    scaledDataCats.coalesce(1, true).saveAsTextFile("./data/scaledDataCatagoriesRDD")

    // train model on scaled data and evaluate metrics
    val lrModelScaledCats = LogisticRegressionWithSGD.train(scaledDataCats, numIterations)

    lrModelScaledCats.save(sc, "./model/LRModel")

    val lrTotalCorrectScaledCats = scaledDataCats.map { point =>
      if (lrModelScaledCats.predict(point.features) == point.label) 1 else 0
    }.sum
    val lrAccuracyScaledCats = lrTotalCorrectScaledCats / numDataCatagories
    val lrPredictionsVsTrueCats = scaledDataCats.map { point =>
      (lrModelScaledCats.predict(point.features), point.label)
    }
    val lrMetricsScaledCats = new BinaryClassificationMetrics(lrPredictionsVsTrueCats)
    val lrPrCats = lrMetricsScaledCats.areaUnderPR
    val lrRocCats = lrMetricsScaledCats.areaUnderROC
    println(f"${lrModelScaledCats.getClass.getSimpleName}\nAccuracy: ${lrAccuracyScaledCats * 100}%2.4f%%\nArea under PR: ${lrPrCats * 100.0}%2.4f%%\nArea under ROC: ${lrRocCats * 100.0}%2.4f%%")

  }
}