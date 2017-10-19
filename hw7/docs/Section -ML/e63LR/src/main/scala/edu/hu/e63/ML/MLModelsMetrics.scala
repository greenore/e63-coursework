package edu.hu.e63.ML

/*
 * MLModelMetrics - Better Metrics for our Models 
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

object MLModelMetrics {
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
    val svmModel = SVMWithSGD.train(data, numIterations)
    val nbModel = NaiveBayes.train(data)
    val dtModel = DecisionTree.train(data, Algo.Classification, Entropy, maxTreeDepth)

    /* Collect Model Metrics */

    val metrics = Seq(lrModel, svmModel).map { model =>
      val scoreAndLabels = data.map { point =>
        (model.predict(point.features), point.label)
      }
      val metrics = new BinaryClassificationMetrics(scoreAndLabels)
      (model.getClass.getSimpleName, metrics.areaUnderPR, metrics.areaUnderROC)
    }

    val LBFGSmetrics = Seq(LBFGSModel).map { model =>
      val scoreAndLabels = data.map { point =>
        (model.predict(point.features), point.label)
      }
      val metrics = new BinaryClassificationMetrics(scoreAndLabels)
      ("Logistic Regression LBFGS", metrics.areaUnderPR, metrics.areaUnderROC)
    }

    val nbMetrics = Seq(nbModel).map { model =>
      val scoreAndLabels = data.map { point =>
        val score = model.predict(point.features)
        (if (score > 0.7) 1.0 else 0.0, point.label)
      }
      val metrics = new BinaryClassificationMetrics(scoreAndLabels)
      (model.getClass.getSimpleName, metrics.areaUnderPR, metrics.areaUnderROC)
    }

    // here we need to compute for decision tree separately since it does 
    // not implement the ClassificationModel interface

    val dtMetrics = Seq(dtModel).map { model =>
      val scoreAndLabels = data.map { point =>
        val score = model.predict(point.features)
        (if (score > 0.5) 1.0 else 0.0, point.label)
      }
      val metrics = new BinaryClassificationMetrics(scoreAndLabels)
      (model.getClass.getSimpleName, metrics.areaUnderPR, metrics.areaUnderROC)
    }

    val allMetrics = metrics ++ nbMetrics ++ dtMetrics ++ LBFGSmetrics
    allMetrics.foreach {
      case (m, pr, roc) =>
        println(f"$m - \n \t Area under PR: ${pr * 100.0}%2.4f%% \n \t Area under ROC: ${roc * 100.0}%2.4f%% \n ")
    }

  }
}