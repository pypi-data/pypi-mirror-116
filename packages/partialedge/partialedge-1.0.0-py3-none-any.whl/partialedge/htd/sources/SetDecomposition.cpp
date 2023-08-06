#include <htd/main.hpp>
#include <htd_io/main.hpp>
#include <htd_cli/main.hpp>

#include <iostream>
#include <fstream>
#include <filesystem>
#include <string>

#include <csignal>
#include <memory>
#include <chrono>

namespace fs = std::filesystem;

//Create a management instance of the 'htd' library in order to allow centralized configuration.
std::unique_ptr<htd::LibraryInstance> manager(htd::createManagementInstance(htd::Id::FIRST));

/**
 * Signal handling procedure.
 */
void handleSignal(int signal)
{
	switch (signal)
	{
	case SIGINT:
	case SIGTERM:
	{
		manager->terminate();

		break;
	}
	default:
	{
		break;
	}
	}

	std::signal(signal, handleSignal);
}

void performDecomposition(htd::ITreeDecompositionAlgorithm* algorithm, std::string inputFile, std::string outputFile)
{
	htd_io::GrFormatImporter importer(manager.get());
	htd::IMultiGraph* graph = importer.import(inputFile);
	htd_io::ITreeDecompositionExporter* exporter = new htd_io::TdFormatExporter();

	if (graph != nullptr && !manager->isTerminated())
	{
		auto* decomposition = algorithm->computeDecomposition(*graph);

		if (decomposition != nullptr)
		{
			if (!manager->isTerminated() || algorithm->isSafelyInterruptible())
			{
				std::ofstream output;
				output.open(outputFile);
				exporter->write(*decomposition, *graph, output);
				output.close();
			}
			else
			{
				std::cerr << "Program was terminated successfully!" << std::endl;
			}

			delete decomposition;
		}
		else
		{
			if (manager->isTerminated())
			{
				std::cerr << "Program was terminated successfully!" << std::endl;
			}
			else
			{
				std::cerr << "NO TREE DECOMPOSITION COMPUTED!" << std::endl;
			}
		}

		delete graph;
	}
	else
	{
		if (manager->isTerminated())
		{
			std::cerr << "Program was terminated successfully!" << std::endl;
		}
		else
		{
			std::cerr << "NO VALID INSTANCE PROVIDED!" << std::endl;
		}
	}
}

int main(int argc, char* argv[])
{
	std::signal(SIGINT, handleSignal);
	std::signal(SIGTERM, handleSignal);

	std::srand(0);

	// Get the default tree decomposition algorithm. One can also choose a custom one.
	htd::ITreeDecompositionAlgorithm* algorithm =
		manager->treeDecompositionAlgorithmFactory().createInstance();

	/**
	 *  Set the optimization operation as manipulation operation in order
	 *  to choose the optimal root reducing height of the tree decomposition.
	 */
	algorithm->addManipulationOperation(new htd::AddEmptyLeavesOperation(manager.get()));
	algorithm->addManipulationOperation(new htd::NormalizationOperation(manager.get()));

	fs::path input_dir = fs::path(argv[1]);
	fs::path output_dir = fs::path(argv[2]);
	for (const auto& set_entry : fs::directory_iterator(input_dir)) 
	{
		fs::path output_set = output_dir / set_entry.path().filename();
		fs::create_directory(output_set);
		for (const auto& graph_entry : fs::directory_iterator(set_entry))
		{
			const auto graph_name = graph_entry.path().stem();

			std::string input_file = graph_entry.path().string();
			std::string output_file = (output_set / (graph_name.string() + ".td")).string();

			performDecomposition(algorithm, input_file, output_file);
		}
	}

	

	return 0;
}
