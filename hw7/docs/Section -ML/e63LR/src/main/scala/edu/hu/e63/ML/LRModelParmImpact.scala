package edu.hu.e63.ML

/*
 * LRModelParmImpact - Impacts of parameters 
 */

import org.apache.spark.rdd.RDD
import org.apache.spark.mllib.optimization.Updater
import org.apache.spark.mllib.optimization.SimpleUpdater
import org.apache.spark.mllib.optimization.L1Updater
import org.apache.spark.mllib.optimization.SquaredL2Updater
import org.apache.spark.mllib.classification.ClassificationModel
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
import org.apache.spark.mllib.util.MLUtils
import java.io.File

object LRModelParmImpact extends App {

  val conf = new SparkConf().setMaster("local[1]").setAppName("LRModelImpact")
  val sc = new SparkContext(conf)

  //Read LabeledPoints Data in to an RDD - Saved from BetterLR

  val LRCuratedData = MLUtils.loadLabeledPoints(sc, "./data/scaledDataCatagoriesRDD/part-00000");

  // cache the data to increase speed of multiple runs agains the dataset
  LRCuratedData.cache;
  val numIterations = 5;
  val myLRHelper = new LRHelper();

  val iterResults = Seq(1, 5, 10, 50).map { param =>
    val model = myLRHelper.LRtrainWithParams(LRCuratedData, 0.0, param, new SimpleUpdater, 1.0)
    myLRHelper.createMetrics(s"$param iterations", LRCuratedData, model)
  }
  println("\nIterations - \n")
  iterResults.foreach { case (param, auc) => println(f"$param, AUC = ${auc * 100}%2.2f%%") }

  // step size
  val stepResults = Seq(0.001, 0.01, 0.1, 1.0, 10.0).map { param =>
    val model = myLRHelper.LRtrainWithParams(LRCuratedData, 0.0, numIterations, new SimpleUpdater, param)
    myLRHelper.createMetrics(s"$param step size", LRCuratedData, model)
  }
  println("\n Steps - \n")
  stepResults.foreach { case (param, auc) => println(f" $param, AUC = ${auc * 100}%2.2f%%") }

  // Regularization
  val regResults = Seq(0.001, 0.01, 0.1, 1.0, 10.0).map { param =>
    val model = myLRHelper.LRtrainWithParams(LRCuratedData, param, numIterations, new SquaredL2Updater, 1.0)
    myLRHelper.createMetrics(s"$param L2 regularization parameter", LRCuratedData, model)
  }
  println("\n Regularization - \n")
  regResults.foreach { case (param, auc) => println(f" $param, AUC = ${auc * 100}%2.2f%%") }

}