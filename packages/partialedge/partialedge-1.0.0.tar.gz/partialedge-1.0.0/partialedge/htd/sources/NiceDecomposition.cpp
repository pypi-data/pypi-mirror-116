#include <htd/main.hpp>
#include <htd_io/main.hpp>
#include <htd_cli/main.hpp>

#include <csignal>
#include <memory>
#include <chrono>

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

int main(int, const char* const* const)
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

	htd_io::GrFormatImporter importer(manager.get());
	htd::IMultiGraph* graph = importer.import(std::cin);
	htd_io::ITreeDecompositionExporter *exporter = new htd_io::TdFormatExporter();

	if (graph != nullptr && !manager->isTerminated())
	{
		auto* decomposition = algorithm->computeDecomposition(*graph);

		if (decomposition != nullptr)
		{
			if (!manager->isTerminated() || algorithm->isSafelyInterruptible())
			{
				exporter->write(*decomposition, *graph, std::cout);
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

	return 0;
}