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

object InitialMLModels {
  def main(args: Array[String]) {

    // Create a Scala Spark Context.

    val conf = new SparkConf().setMaster("local[*]").setAppName("All Models")
    val sc = new SparkContext(conf)

    // Read the train file , its a tsv file with header
    // Remove header and split on tabs

    val rawtrainrdd = sc.textFile("./data/train.tsv")
    val header = rawtrainrdd.first()
    val trainrdd = rawtrainrdd.filter(_!= header)
    val cleantrainrdd = trainrdd.map(_.split("\t"))

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
    val numIterations = 10
    val maxTreeDepth = 5

    val LogisticRegressionWithLBFGS = new LogisticRegressionWithLBFGS
    val LBFGSModel = LogisticRegressionWithLBFGS.run(data)

    val lrModel = LogisticRegressionWithSGD.train(data, numIterations)
    val svmModel = SVMWithSGD.train(data, numIterations)
    val nbModel = NaiveBayes.train(data)
    val dtModel = DecisionTree.train(data, Algo.Classification, Entropy, maxTreeDepth)

    
    /* Logistic Regression */

    // make prediction on a single data point
    val dataPoint = data.first
    println("Data Point" + dataPoint)
    val prediction = lrModel.predict(dataPoint.features)
    println("Prediction" + prediction)
    val trueLabel = dataPoint.label
    println("True Label" + trueLabel)
  
    
    // make prediction on all data point

    val predictions = lrModel.predict(data.map(lp => lp.features))

    // compute accuracy for logistic regression

    val lrTotalCorrect = data.map { point =>
      if (lrModel.predict(point.features) == point.label) 1 else 0
    }.sum

    // accuracy is the number of correctly classified examples (same as true label)
    // divided by the total number of examples
    val lrAccuracy = lrTotalCorrect / numData

    // compute accuracy for the other models

    val LBFGSTotalCorrect = data.map { point =>
      if (LBFGSModel.predict(point.features) == point.label) 1 else 0
    }.sum
    val svmTotalCorrect = data.map { point =>
      if (svmModel.predict(point.features) == point.label) 1 else 0
    }.sum
    val nbTotalCorrect = data.map { point =>
      if (nbModel.predict(point.features) == point.label) 1 else 0
    }.sum
    // decision tree threshold needs to be specified
    val dtTotalCorrect = data.map { point =>
      val score = dtModel.predict(point.features)
      val predicted = if (score > 0.5) 1 else 0
      if (predicted == point.label) 1 else 0
    }.sum
    val svmAccuracy = svmTotalCorrect / numData

    val nbAccuracy = nbTotalCorrect / numData

    val dtAccuracy = dtTotalCorrect / numData

    val LBFGSAccuracy = LBFGSTotalCorrect / numData

    println("Model Accuracy Summary")
    println("===========================")
    println("SVM Accuracy = " + svmAccuracy)
    println("NB Accuracy = " + nbAccuracy)
    println("DT Accuracy = " + dtAccuracy)
    println("LR Accuracy = " + lrAccuracy)
    println("LRLBFGS Accuracy = " + LBFGSAccuracy)

  }
}