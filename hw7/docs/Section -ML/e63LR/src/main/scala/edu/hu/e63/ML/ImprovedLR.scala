package edu.hu.e63.ML

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

object ImprovedLR {
  def main(args: Array[String]) {

    // Create a Scala Spark Context.

    val conf = new SparkConf().setMaster("local[*]").setAppName("All Models")
    val sc = new SparkContext(conf)

    // Read the train file , its a tsv file with header
    // Remove header and split on tabs

    val rawtrainrdd = sc.textFile("./data/train.tsv")
    val header = rawtrainrdd.first()
    val trainrdd = rawtrainrdd.filter(_ != header)
    val cleantrainrdd = trainrdd.map(x => x.split("\t"))

    /* Data RDD is LabeledPoint RDD created with  
     * a) cleaning up quotes 
     * b) Defining a  label col 26
     * c) Defining features - cols 5-25  
     * d) Removing -ve values and replacing "?" with 0.0
    */
    val data = cleantrainrdd.map { r =>
      val trimmed = r.map(_.replaceAll("\"", "")) // Trim quotes
      val label = trimmed(r.size - 1).toInt // Get label
      val features = trimmed.slice(4, r.size - 1) // Get features
        .map(d => if (d == "?") 0.0 else d.toDouble) // Clean "?"
        .map(d => if (d < 0) 0.0 else d) // Clean -ve numbers
      LabeledPoint(label, Vectors.dense(features))
    }

    data.cache

    val numData = data.count
    val numIterations = 20
    val maxTreeDepth = 5

    val LogisticRegressionWithLBFGS = new LogisticRegressionWithLBFGS
    val LBFGSModel = LogisticRegressionWithLBFGS.run(data)

    val lrModel = LogisticRegressionWithSGD.train(data, numIterations)

    /* Metrics */

    val vectors = data.map(lp => lp.features)
    val matrix = new RowMatrix(vectors)
    val matrixSummary = matrix.computeColumnSummaryStatistics()

    println("Matrix Summary Mean" + matrixSummary.mean)
    println(matrixSummary.min)
    println(matrixSummary.max)
    println(matrixSummary.variance)
    println(matrixSummary.numNonzeros)

    // scale the input features using MLlib's StandardScaler

    val scaler = new StandardScaler(withMean = true, withStd = true).fit(vectors)
    val scaledData = data.map(lp => LabeledPoint(lp.label, scaler.transform(lp.features)))
    // compare the raw features with the scaled features
    println(data.first.features)
    println(scaledData.first.features)

    
    /* Check Avg */

    // train a logistic regression model on the scaled data, and compute metrics

    //val lrModelScaled = LogisticRegressionWithSGD.train(scaledData, numIterations)
    val lrModelScaled = LogisticRegressionWithSGD.train(scaledData, numIterations)
    val lrTotalCorrectScaled = scaledData.map { point =>
      if (lrModelScaled.predict(point.features) == point.label) 1 else 0
    }.sum
    val lrAccuracyScaled = lrTotalCorrectScaled / numData
    val lrPredictionsVsTrue = scaledData.map { point =>
      (lrModelScaled.predict(point.features), point.label)
    }
    val lrMetricsScaled = new BinaryClassificationMetrics(lrPredictionsVsTrue)
    val lrPr = lrMetricsScaled.areaUnderPR
    val lrRoc = lrMetricsScaled.areaUnderROC
    println(f"${lrModelScaled.getClass.getSimpleName} - \nAccuracy: ${lrAccuracyScaled * 100}%2.4f%%\nArea under PR: ${lrPr * 100.0}%2.4f%%\nArea under ROC: ${lrRoc * 100.0}%2.4f%%")

  }
}